from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
from _get_model import *
#kernel_gauss = 5


def squared_error(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true))


def gauss2D(shape=(5,5),sigma=0.5):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def define_masked_model(height, width, channel=1,out_channel=1,kernel_size=5, sigma=1):
    num_u = [32, 32, 32, 32, 32]#original [128, 128, 128, 128, 128]
    num_d = [32, 32, 32, 32, 32] #[128, 128, 128, 128, 128]
    kernel_u = [3, 3, 3, 3, 3]
    kernel_d = [3, 3, 3, 3, 3]
    num_s = [4, 4, 4, 4, 4]
    kernel_s = [1, 1, 1, 1, 1]
    lr = 0.001
    inter = "bilinear"

    base_model = define_model(num_u, num_d, kernel_u, kernel_d, num_s, kernel_s, height, width, inter, lr, input_channel=channel,
                             out_channel=out_channel)
    #kernel_size = kernel_gauss 
    #Kernel Gauss: Detect specific masked regions from gaussian distribution 
    kernel_weights = gauss2D(shape=(kernel_size,kernel_size), sigma=sigma)
    
    kernel_weights = np.expand_dims(kernel_weights, axis=-1)
    kernel_weights = np.repeat(kernel_weights, out_channel, axis=-1)
    kernel_weights = np.expand_dims(kernel_weights, axis=-1) 
    
    x = base_model.output
    g_layer = DepthwiseConv2D(kernel_size, use_bias=False, padding='same')
    g_layer_out = g_layer(x)
    g_layer.set_weights([kernel_weights])
    g_layer.trainable = False 
    
    base_model_ = Model(base_model.input, g_layer_out)
    
    masked_image = Input(shape=(height, width, out_channel))
    mask_image = Input(shape=(height, width, 1))

    loss = Lambda(lambda x: K.sum(K.square((x[0] - x[1]) * x[2]), axis=-1))([base_model_.output, masked_image, mask_image])
    
    model = Model([base_model_.input, masked_image, mask_image], loss)
    model.compile(loss="mean_absolute_error", optimizer=Adam(lr=lr))
    #model.summary()
    #base_model.summary()
    #base_model.save('my_model.h5')
    
    return model, base_model, base_model_
   
def demask_multiple(image,mask_image, init_image=None, num_iter = 300, kernel_size=10, sigma=5,verbose=0):
    '''
    image: (H,W,C), spatial image
    mask_image: mask of 'spatial image'.
    '''
    height, width = image.shape[:2]
    n_features = image.shape[2]
    if init_image.all()==None:
        channels = 1
        model, base_model,base_model_ = define_masked_model(height, width, channel = channels, out_channel = n_features,  
                                                kernel_size=kernel_size, sigma=sigma)
        input_noise = np.random.uniform(0, 0.1, (1, height, width, 1))
    else:
        channels = init_image.shape[2]
        model, base_model,base_model_ = define_masked_model(height, width, channel=channels,out_channel=n_features,
                                                kernel_size=kernel_size, sigma=sigma)
        input_noise = init_image[None, :, :, :]
        
    outlabel = np.zeros((1,height,width))
    
    if verbose:
        plt.ion()
    for i in range(num_iter):
        model.train_on_batch([init_image[None, :, :, :], 
                              image[None, :, :, :], 
                              mask_image[None, :, :, None]], outlabel)
        if verbose:
             if i % 100==0:
                outimg = base_model.predict(init_image[None, :, :, :])[0]
                outimg_ = base_model_.predict(init_image[None, :, :, :])[0]
                plt.subplot(1,2,1)
                plt.imshow(outimg[:,:,0])
                plt.title(("Iteration:"+str(i+1)))
                plt.subplot(1,2,2)
                plt.imshow(outimg_[:,:,0])
                plt.title(("Iteration:"+str(i+1)))
                plt.show()
    return base_model.predict(input_noise)[0], base_model_.predict(input_noise)[0]
    