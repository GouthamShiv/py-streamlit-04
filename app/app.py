import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image

st.title('NFL Football Stats (Rushing) Explorer')
image = Image.open('./app/NFL_logos.jpg')
st.image(image, use_column_width=True, caption='NFL Football team logos')
