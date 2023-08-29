# from TOKEN import TOKEN
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram import Dispatcher, Bot, executor, types
#
#
# bot = Bot(TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
#
# media_group = []
# text = 'some caption for album'
#
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await bot.send_message(message.chat.id, 'WELCOME')
#     for num in range(3):
#         media_group.append(types.InputMediaPhoto(open('i5.jpg', 'rb'), caption = text if num == 0 else ''))
#     await bot.send_media_group(chat_id=message.chat.id, media=media_group)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp)

# Importing Image class from PIL module
from PIL import Image

# Opens a image in RGB mode
im = Image.open(f"d:\Python_IT_School\Groccery Bud\images\dog1.jpg")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size

# Setting the points for cropped image
left = 4
top = height / 5
right = 154
bottom = 3 * height / 5

# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
newsize = (300, 300)
im1 = im1.resize(newsize)
# Shows the image in image viewer
im1.show()




