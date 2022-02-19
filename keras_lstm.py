
from keras.models import Sequential
from keras.layers import Dense, LSTM
def lstm_train(X,Y):
    #X ve Y ile ML egitilir ve model dondurulur.

    model = Sequential()
    #model.add(Embedding(n_unique_words, 128, input_length=maxlen))
    model.add(LSTM(64,activation='relu',
               input_shape=(67, 1), return_sequences=True))
    #model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(X, Y, epochs=2, batch_size=1, verbose=2)

    return model