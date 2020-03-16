import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import mean_squared_error
import numpy as np

changed_lr = False
folder_name = "my_model"


if __name__ == "__main__":
    df = pd.read_csv("entropy.csv")
    X = df["Input"].values
    y = df["Output"].values
    file_name = "Final_values.csv"
    MAX_EPOCHS = 2000
    BATCH = 100
    X_train, X_testing, y_train, y_testing = train_test_split(X, y, test_size=0.2)
    X_test, X_val, y_test, y_val = train_test_split(X_testing, y_testing, test_size=0.5)
    # Change the shape of all
    X_train = X_train.reshape((len(X_train), 1, 1))
    X_test = X_test.reshape((len(X_test), 1, 1))
    y_train = y_train.reshape((len(y_train), 1, 1))
    y_test = y_test.reshape((len(y_test), 1, 1))
    X_val = X_val.reshape((len(X_val), 1, 1))
    y_val = y_val.reshape((len(y_val), 1, 1))
    model = keras.Sequential()
    model.add(layers.SimpleRNN(4, return_sequences=True))
    model.add(layers.SimpleRNN(4))
    model.add(layers.Dense(1, activation=tf.keras.activations.sigmoid))
    model.compile(loss=tf.keras.losses.MeanAbsoluteError(),
                  optimizer=tf.keras.optimizers.Adam(1e-4),
                  metrics=['mae'])
    model.fit(X_train, y_train, epochs=MAX_EPOCHS, batch_size=BATCH, verbose=1,
              validation_data=(X_test, y_test))
    y_pred = model.predict(X_val)
    rmse_calculated = mean_squared_error(y_pred.flatten(), y_val.flatten())
    print(f"RMSE on Validation: {rmse_calculated}")
    final_save_matrix = np.stack((X_val.flatten(), y_val.flatten(), y_pred.flatten()), axis=1)
    open(file_name, 'w').close()
    np.savetxt(file_name, final_save_matrix,
               delimiter=',', header="X_validation,Original_Y,Predicted_y", comments="")
    # os.remove(file_name)
    model.save(folder_name, save_format='tf')
    # Noted RMSE: 9.070411888314994e-06