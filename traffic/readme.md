# Traffic Sign Classification - Experimentation

## What I Tried
reading documentation of Tensorflow and selecting Conv2D for building a image processinga architecture
input layers were required with the issued image shape
and flatten layer was required to turn the model to a workable form(was showing error before)
the compile optimizer was set to optimizers.Adam with learning rate of 0.001

## What Worked Well
[changing the convolutional layers into convolutional blocks helped the accuracy drastically.
 The minimum number of filters were set to 32 and each subsequent block would double the number of filters 64 to potentially 128 if another block is to be added]

## What Didn't Work
although simple Convolutional layer(1-3) were working good for the 3 unit sample(70-80% accuracy) they were terrible at the 43 units sample(6-7% accuracy)

## Results

### Architecture 1
```python
# Your TensorFlow/Keras model code here
model = tf.keras.Sequential([
    layers.Conv2D(filters = 32, kernel_size = (7, 7), input_shape = (IMG_HEIGHT, IMG_WIDTH, 3), activation="relu"),

    layers.Conv2D(filters= 64, kernel_size = (5,5)),

    layers.Conv2D(filters= 128, kernel_size = (3, 3)),

    layers.MaxPool2D(pool_size=(4,4)),

    layers.Flatten(),

    layers.Dense(units=NUM_CATEGORIES, activation="softmax")
])
```
**Accuracy**: [0.0573]  
**Notes**: [terrible at the 43 units sample. starting at 32 filters for the larger sample]

### Architecture 2
```python
# Your TensorFlow/Keras model code here
model = tf.keras.Sequential([
    layers.Conv2D(filters = 32, kernel_size = (7, 7), input_shape = (IMG_HEIGHT, IMG_WIDTH, 3), activation="relu"),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),

    layers.Dense(units=NUM_CATEGORIES, activation="softmax")
])
```
**Accuracy**: [0.9670]  
**Notes**: [switching from covolution layers to a held together block proved much better, although suspects of overfitting are possible]

### Architecture 3
```python
# Your TensorFlow/Keras model code here
model = tf.keras.Sequential([
    layers.Conv2D(filters = 32, kernel_size = (7, 7), input_shape = (IMG_HEIGHT, IMG_WIDTH, 3), activation="relu"),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),

    layers.Dense(units=NUM_CATEGORIES, activation="softmax")
])
```
**Accuracy**: [0.9817]  
**Notes**: [adding a second covolutional block further increases the accuracy, still risk of overfitting is present. BatchNormalization is added for more stable training]

### Architecture 4
```python
# Your TensorFlow/Keras model code here
model = tf.keras.Sequential([
         layers.Conv2D(filters = 32, kernel_size = (7, 7), input_shape = (IMG_HEIGHT, IMG_WIDTH, 3), activation="relu"),
         layers.BatchNormalization(),
         layers.Conv2D(32, (3, 3), activation='relu'),
         layers.MaxPooling2D(2, 2),
         layers.Dropout(rate=0.5),

         layers.Conv2D(64, (3, 3), activation='relu'),
         layers.BatchNormalization(),
         layers.Conv2D(64, (3, 3), activation='relu'),
         layers.MaxPooling2D(2, 2),
         layers.Dropout(rate=0.5),

         layers.Flatten(),

         layers.Dense(units=NUM_CATEGORIES, activation="softmax")
])
```
**Accuracy**: [0.9812]  
**Notes**: [Adding Dropout rate to remove overfitting, added GlobalAveragePooling2D for reducung overfitting]