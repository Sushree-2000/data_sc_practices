import numpy as np
import tensorflow as tf
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# ---- Fix randomness ----
SEED = 42
np.random.seed(SEED)
random.seed(SEED)
tf.random.set_seed(SEED)

# ---- Dummy data ----
x = np.random.rand(100, 20)
y = x.copy()

# ---- Model 1 ----
model1 = Sequential([
    Dense(10, activation="relu", input_shape=(20,)),
    Dense(20)
])
model1.compile(optimizer="adam", loss="mse")

history1 = model1.fit(
    x, y,
    epochs=2,
    batch_size=16,
    shuffle=True,
    validation_split=0.2
)

# ---- Reset seeds again ----
np.random.seed(SEED)
random.seed(SEED)
tf.random.set_seed(SEED)

# ---- Model 2 ----
model2 = Sequential([
    Dense(10, activation="relu", input_shape=(20,)),
    Dense(20)
])
model2.compile(optimizer="adam", loss="mse")

history2 = model2.fit(
    x, y,
    shuffle=True,
    epochs=2,
    batch_size=16,
    validation_split=0.2
)

# ---- Compare weights ----
for i, (w1, w2) in enumerate(zip(model1.get_weights(), model2.get_weights())):
    print(f"Layer {i} equal:", np.allclose(w1, w2))
