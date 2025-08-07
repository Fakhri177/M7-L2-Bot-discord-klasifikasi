import discord
from discord.ext import commands
import os, random
import requests
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def clasify(ctx):
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            file_name = file.filename
            file_url = file.url
            await file.save(f'./{file_name}')
            await ctx.send(f'File berhasil disimpan dengan nama {file_name}')
            await ctx.send(f'Dapat juga di akses melalui cloud discord di {file_url}')
            
            kelas, skor = get_class('keras_model.h5', 'labels.txt', f'./{file.filename}')

            #INFERENSI :
            if kelas == "pipit" and skor >= 0.75:
                await ctx.send('Nama : Pipit')
                await ctx.send('Makanan : kecambah, jagung, buah')
                await ctx.send('Habitat Asli : Burung pipit (terutama dari keluarga Passeridae) berasal dari daerah Eropa, Asia, dan Afrika')
                await ctx.send('Tempat Favorit : Padang rumput, Hutan terbuka, Area pertanian, Permukiman manusia (bahkan di kota besar)')

            elif kelas == 'merpati' and skor >= 0.75:
                await ctx.send('Nama : Merpati')
                await ctx.send('Makanan : Biji-bijian, sayuran hijau, dan buah-buahan')
                await ctx.send('Habitat Asli : Merpati liar berasal dari Eropa, Afrika Utara, hingga Asia Selatan. Spesies leluhur merpati peliharaan adalah Columba livia (Rock Pigeon).')
                await ctx.send('Tempat Favorit : Tebing berbatu (di alam liar), Bangunan kota (sebagai pengganti tebing), Pedesaan dan perkotaan')


            elif kelas == 'burung hantu' and skor >= 0.75:
                await ctx.send('Nama : Burung hantu')
                await ctx.send('Makanan : tikus, belalang, ikan, ayam')
                await ctx.send('Habitat Asli : Burung hantu tersebar luas di seluruh dunia (kecuali Antartika), tergantung pada jenisnya. Ada lebih dari 200 spesies burung hantu.')
                await ctx.send('Tempat Favorit : Hutan lebat, Savana, Pegunungan, Gurun, Pedesaan & bahkan kota (beberapa jenis seperti burung hantu gudang)')

            else:
                await ctx.send('Gambar tidak di ketahui, mohon kirim gambar burung (pipit/merpati/burung hantu)')


    else:
        await ctx.send('Kamu tidak melampirkan apa-apa!')

bot.run("Masukkan Token")