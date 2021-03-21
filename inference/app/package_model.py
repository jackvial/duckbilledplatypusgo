import os
import tarfile

from transformers import AutoTokenizer, AutoModelForSequenceClassification

if __name__ == "__main__":
    pretrained_model = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
    model = AutoModelForSequenceClassification.from_pretrained(pretrained_model)
    
    model_path = 'model/'
    model.save_pretrained(save_directory=model_path)
    tokenizer.save_pretrained(save_directory=model_path)

    # zipped_model_path = os.path.join(model_path, "model.tar.gz")

    # with tarfile.open(zipped_model_path, "w:gz") as tar:
        
    #     # Model the model to be deployed
    #     tar.add(model_path)
        
    #     # Bundle inference code and requirements to be deployed
    #     tar.add(code_path)