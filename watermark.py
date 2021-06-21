import os
from PIL import ImageFont,ImageDraw,Image
text = "第五届强网杯专用"
# 灰色
color = (0x8f,0x8f,0x8f)
rot = 10
def gen_watermark():
    width = 1500
    height = 1500
    watermark = Image.new('RGBA',(width,height),(0,0,0,0))
    font = ImageFont.truetype('fs.ttf',33) 
    draw = ImageDraw.Draw(watermark)
    
    side_width = len(text) * 33 + 50
    side_height =  80
    
    for i in range(width // side_width << 2):
        for j in range(height // side_height << 2):
            draw.text((i*side_width,j*side_height),text,font=font,fill=color)
    
    watermark = watermark.rotate(rot, expand=1)
    watermark = watermark.crop((width//2-width//4,height//2-height//4,width//2 + width//4, height//2 + height//4))
    watermark = watermark.resize((width,height))
    watermark.save('watermark.png')
    

def watermark(background,waterimage,output_path):
    print('Generate watermark now...')
    bg = Image.open(background)
    wm = Image.open(waterimage)
    wm = wm.resize(bg.size)
    # 使水印居中
    width1,height1 = bg.size
    width2,height2= wm.size
    width = (width1-width2)//2
    height = (height1-height2)//2
    # 转换为rgba模式
    if bg.mode != "RGBA":
        bg = bg.convert("RGBA")
    if wm.mode != "RGBA":
        wm = wm.convert("RGBA")
    # 创建新图层
    layer = Image.new("RGBA",bg.size,(0,0,0,0))
    # 合并水印文件
    layer.paste(wm,(width,height))
    out = Image.composite(layer,bg,layer)
    # 重命名保存文件
    out.save(output_path)
    print('Generate watermark done!')

def init():
    print('Initalize workspace now...')
    try:
        os.mkdir('input')
    except Exception as e:
        print(e)
    os.system('mv *.png input/')
    try:
        os.mkdir('output')
    except Exception as e:
        print(e)
    
    
def clean():
    print("clean workspace now")
    os.system('rm watermark.png')
    print("clean done!")

def main():
    init()
    gen_watermark()
    
    print(f"now we at {os.getcwd()}")
    cwd = os.getcwd()
    for inp in os.listdir('./input'):
        input_path = os.path.join(cwd,'input',inp)
        output_path = os.path.join(cwd,'output',inp)
        watermark(input_path,'watermark.png', output_path)
    clean()

if __name__ == "__main__":
    main()

