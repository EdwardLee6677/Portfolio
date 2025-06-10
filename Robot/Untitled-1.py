# %%
import numpy as np
import cv2
import pandas as pd

# %%
data = np.load('bottle.npy', allow_pickle=True)
robot_state = data[0]['robot_state']

# %%
df = pd.DataFrame(robot_state)
df.to_csv('data.csv')

# %%
data2 = np.load('bottle_2traj.npy', allow_pickle=True)
image = np.append(data2[0]['image'], data2[1]['image'], axis=0)
other = np.append(data2[0]['other'], data2[1]['other'])
hand_image = np.append(other[0]['hand_image'], other[1]['hand_image'], axis=0)
third_person_image = np.array(np.append(other[0]['third_person_image'], other[1]['third_person_image'], axis=0), dtype=np.uint8)

# %%
print(image.shape)

# %%
for i in range(image.shape[0]):
    cv2.imshow('img', image[i])
    cv2.imshow('hand', hand_image[i])
    cv2.imshow('third', third_person_image[i][:, :, :3])
    cv2.waitKey(33)
cv2.destroyAllWindows()

# %%
print(data[0].keys())


