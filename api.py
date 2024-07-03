import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from parsing import main

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def read_csv(file: str) -> list[list[str, str, str, str]]:
    df = pd.read_csv(file, header=None)
    return df.values.tolist()


@app.get("/api/v1/allNews")
def get_all_news() -> list[dict]:
    news = read_csv("news_selenium.csv")

    response = [
        {
            'category': n[0],
            'title': n[1],
            'link': n[2],
            'description': n[3]
        }
        for n in news
    ]

    return response


@app.get("/api/v1/runParser")
def run_parser() -> dict:
    response = {"status": ""}
    try:
        main()
        response["status"] = 'success'
    except Exception as e:
        ...
        response["status"] = 'failed'
        response["message"] = 'Что-то пошло не так'

    return response


@app.get("/api/healthCheck")
def health_check() -> dict:
    return {"status": "success"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)

    # uvicorn api:app --reload --host=127.0.0.1 --port 5000
