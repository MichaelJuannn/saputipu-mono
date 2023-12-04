from transformers import BertTokenizer, TFBertModel
import keras

def predict(data: str):
    tokenizer = BertTokenizer.from_pretrained('./src/assets/')
    model = keras.models.load_model('./src/model/scam_class.h5',custom_objects={"TFBertModel": TFBertModel})
    encoded = tokenizer(text=data,add_special_tokens=True,max_length=50,padding='max_length',
                        truncation=True,return_tensors='tf',return_token_type_ids=False,verbose=True,return_attention_mask=True)
    input_obj = {'input_ids': encoded['input_ids'], 'attention_mask': encoded['attention_mask']}
    prediction = model.predict(input_obj)
    return prediction

result = predict("Mainkan terus games mu sekarang dan beli koinnya pakai pulsamu, cek caranya di http://tsel.me/jajanonline")
print(result)