from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, TFBertModel
import keras
import traceback

class Prediction(BaseModel):
    text: str

app = FastAPI()
tokenizer = BertTokenizer.from_pretrained('./assets/')
model = keras.models.load_model('./model/scam_class.h5',custom_objects={"TFBertModel": TFBertModel})

@app.get("/")
async def root():
    text = "Mainkan terus games mu sekarang dan beli koinnya pakai pulsamu, cek caranya di http://tsel.me/jajanonline"
    encoded = tokenizer(text=text,add_special_tokens=True,max_length=50,padding='max_length',
                        truncation=True,return_tensors='tf',return_token_type_ids=False,verbose=True,return_attention_mask=True)
    input_obj = {'input_ids': encoded['input_ids'], 'attention_mask': encoded['attention_mask']}
    prediction = model.predict(input_obj)
    print(type(prediction))
    pred_arr = prediction.tolist()
    print(type(pred_arr))
    output = {
        "neutral": prediction[0][0],
        "scam": prediction[0][1],
        "spam": prediction[0][2]
    }
    return {"result":pred_arr}
@app.post("/predict")
async def predict(data: Prediction):
    try:
        text = data.text
        encoded = tokenizer(text=text,add_special_tokens=True,max_length=50,padding='max_length',
                            truncation=True,return_tensors='tf',return_token_type_ids=False,verbose=True,return_attention_mask=True)
        input_obj = {'input_ids': encoded['input_ids'], 'attention_mask': encoded['attention_mask']}
        prediction = model.predict(input_obj)
        pred_arr = prediction.tolist()
        return {"neutral": pred_arr[0][0], "scam": pred_arr[0][1], "spam": pred_arr[0][2]}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong")