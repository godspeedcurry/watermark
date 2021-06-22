#!/usr/bin/env python3
import os
from PIL import ImageFont,ImageDraw,Image
text = "第五届强网杯专用"
# 灰色
color = (0x8f,0x8f,0x8f)
rot = 10
def gen_watermark():
    print('Generate watermark now...')
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
    print('Generate watermark done!')

def watermark(background,waterimage,output_path):
    print(f'deal {output_path}, please wait')
    bg = Image.open(background)
    wm = Image.open(waterimage)
    wm = wm.resize(bg.size)
    # 使水印居中
    width1,height1 = bg.size
    width2,height2= wm.size
    width = (width1-width2) // 2
    height = (height1-height2) // 2
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
    

def init():
    print('Initalize workspace now...')
    os.system('rm -rf ./input')
    os.system('rm -rf ./output')


    try:
        os.mkdir('tmp')
    except Exception as e:
        print(e)
    os.system('mv *.png *.jpg tmp/')
    
    try:
        os.mkdir('input')
    except Exception as e:
        print(e)
    
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
    cwd = os.getcwd()
    # convert format now
    for tp in os.listdir('./tmp'):
        if 'DS_Store' in tp:
            continue
        orgin_path = os.path.join(cwd, 'tmp', tp)
        img = Image.open(orgin_path)
        if orgin_path.endswith('.png'):
            os.system(f'mv ./tmp/{tp} ./input/{tp}')
            print(f'{orgin_path} move success')
        else:
            input_path = os.path.join(cwd,'input',tp.split('.')[0]+".png")
            img.save(input_path)
            print(f'{input_path} convert success')
    gen_watermark()
    
    print(f"now we at {cwd}")
    
    for inp in os.listdir('./input'):
        input_path = os.path.join(cwd,'input',inp)
        output_path = os.path.join(cwd,'output',inp)
        watermark(input_path,'watermark.png', output_path)
    clean()

if __name__ == "__main__":
    main()

