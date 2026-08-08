import re

html = open("tunnelrush.html").read()

bad_play_button_2 = re.search(r'Oe\.jsxDEV\("button",\{onClick:B,disabled:T,className:"px-8 py-4 bg-cyan-500 hover:bg-cyan-400 text-black font-bold rounded-full text-2xl transition-all hover:scale-105 hover:shadow-\[0_0_30px_rgba\(0,255,255,0\.6\)\] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed w-full max-w-sm",children:T\?"CHECKING...":"START GAME"\}', html)
if bad_play_button_2:
    new_play_button_2 = bad_play_button_2.group(0).replace('onClick:B,disabled:T,', 'onClick:B,onTouchStart:(e)=>{if(!T){e.preventDefault();B();}},disabled:T,')
    html = html.replace(bad_play_button_2.group(0), new_play_button_2)
    open("tunnelrush.html", "w").write(html)
    print("START GAME button updated")
else:
    print("Not found 2")
