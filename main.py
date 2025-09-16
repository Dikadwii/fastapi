#import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel 
import pandas as pd
from datetime import datetime

#membuat objek fastAPI
app = FastAPI()

password ="kopigaeinspirasi12"


#membuat endpoint -> ketentuan untuk client membuat request
#function (get, put ,post, delete)
#url (/...)

#endpoint pertama/root untuk mendapatkan pesan "selamat datang "
@app.get("/")
def getWelcome():#function untuk menghandle endpoint diatas
    return {
        "msg":"selamat datang!"
    }

#endpoint untuk menampilkan semua dataset
@app.get("/data")
def GetData():
    #melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    #mengembalikan response isi dataset
    return df.to_dict(orient="records")

#routing/path parameter -> url dinamis -> menyesuaikan dengan data yang ada di server
#endpoint untuk menampilkan data sesuai lokasi
#data dari rusia -> /data/rusia
#data dari Zimbabwe -> /data/zimbabwe
@app.get("/data/{location}")
def getData(location: str):
    #melakukan prosess mengambil data dari csv
    df = pd.read_csv("dataset.csv")

    #filter data berdasarkan parameter
    result = df[df.location == location]

    #validate hasil ada
    if len(result) == 0:
        #menampilkan pesan eror -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found")

    #mengambil response isi dataset
    return df.to_dict(orient="records")

@app.delete("/data/{id}")
def deleteData(id: int, api_key: str = Header(None)):
    #PROSES AUTENTICATION
    if api_key != None or api_key == password:
        #kalau ada lanjut ke proses delete
        #kalau tidak ada kasih pesan -> tidak ada akses
        raise HTTPException(status_code=401, detail="you don't have acces!")


    df = pd.read_csv("dataset.csv")
    

    #cek apakah datanya sudah ada
    result = df[df.id == id]

    #validate hasil ada
    if len(result) == 0:
        #menampilkan pesan eror -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found")


   
   #proses hapus data
   #condition
    result = df[df.id != df]
    result.to_csv("dataset.csv", index=False)

    return{
        "msg": "Data has been deleted!"
    }

class profile(BaseModel):
    name: str
    age: int
    location: str


#endpoint untuk nambah data baru
@app.post("/data/{id}")
def createData(profile: profile):
    df = pd.read_csv("dataset.csv")


    NewData = pd.DataFrame({
        "id": (profile.id),
        "name": (profile.name),
        "age": (profile.age),
        "location": (profile.location),
        "created_at": (datetime.now().date()),


    })
   

    print(profile)

    df = pd.concat([df, NewData])

    df.to_csv("dataset.csv", index=False)

    return{
        "msg":"data has been created"
    }
 