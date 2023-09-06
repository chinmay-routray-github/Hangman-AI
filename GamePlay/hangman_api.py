
from predict import Prediction
from fastapi import FastAPI, status, Query, HTTPException, Security, Header
from fastapi.security import APIKeyHeader
from typing import Optional, List
import uvicorn
from auth import get_api_key

app = FastAPI()


class Hangman_API:

    def __init__(self):
        self.predict = Prediction()
        

    @app.get("/Hangman-AI/game/guess/{word}/{guess_list}", status_code=status.HTTP_200_OK)
    async def guess_letter(word : str, guess_list : str = None, 
                           api_key:str = Security(get_api_key)):

        # checking input hidden word
        for s in word:
            if s not in Hangman_API().predict.char_to_id:
                raise HTTPException(detail = "Please check the input. It may not contain English letters",
                                status_code= status.HTTP_406_NOT_ACCEPTABLE)
            
        # pre-procesiing the guess list

        guess_list = list(guess_list) if guess_list != ' ' else []
        
        # prediction
        response = Hangman_API().predict.guess(word, guess_list)
        print(response)
        try:
            return response
        except:
            raise HTTPException(detail = "Please check the input. It may not be proper",
                                status_code= status.HTTP_406_NOT_ACCEPTABLE)


if __name__ == '__main__':
    uvicorn.run("hangman_api:app", host='127.0.0.1', port=8000, reload = True)
    
    