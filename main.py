from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2 
import json

import fitz

print(fitz.__doc__)

window = Tk();
filename = ""
win_width = window.winfo_screenwidth()
win_height = window.winfo_screenheight()

#print(" {w} {h}".format(w=win_width,h=win_height))
window.title('Pdf key finder')
#window.geometry("{w}x{h}".format(w=win_width,h=win_height))
window.config(bg='white')
frame = Frame(window,bg='#00ff88')
frame.grid(row=0,column=0)

key_var = StringVar()
value_var = StringVar()





photo = PhotoImage(file = r"D:\flutter1\pdf_key_finder_in_python\upload.png",width=50,height=50)


key_label = Label(frame,text="Enter a Key",bg='#00ff88')
key_label.grid(row=0,column=0)

frame_image = Frame(frame)
frame_image.grid(row=3,column=0,columnspan=3)

#tkimg = PhotoImage(file=r'D:\flutter1\pdf_key_finder_in_python\page-0.png')

view_image = Label(frame_image,bg="#00ff88")
view_image.grid(row=0,column=0,columnspan=3)

view_text = Label(frame,bg="#ffffff", justify='left')
view_text.grid(row=0,column=4,rowspan=4)


def callback(sv):
    print(sv.get())
    try:
      value = output[sv.get()]
      print(value)
      value_var.set(value)  
      pass
    except Exception:
      pass
        

key_var.trace("w", lambda name, index,mode, var=key_var: callback(var))



key_entry = Entry(frame,textvariable=key_var)
key_entry.grid(row=0,column=1)


value_label = Label(frame,text="Enter a Value",bg='#00ff88')
value_label.grid(row=1,column=0)

value_entry = Entry(frame,textvariable=value_var)
value_entry.grid(row=1,column=1)

upload_button = Button(frame,text='upload',image=photo,compound=LEFT)
upload_button.grid(row=0,column=2,rowspan=2)

output = {
    'retailer_name':'',
    'retailer_address':'',
    'retailer_gstin':'',
    'retailer_pan':'',
    'invoice_number':'',
    'invoice_date':'',
    'description_of_services':'',
    'sac':'',
    'amount':'',
    'cgst':'',
    'sgst':'',
    'igst':'',
    'total':'',
    'otp':''
}
def upload():
    global output
    global filename
    filename = askopenfilename() 
    print(filename)
    #window.config(title=filename)
    
    doc = fitz.open('{f}'.format(f=filename))
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save("page-%i.png" % page.number)
    
    pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix  # PPM does not support transparency
    imgdata = pix1.tobytes("ppm")  # extremely fast!
    tkimg = PhotoImage(data = imgdata)
    #tkimg = PhotoImage(file=r"page-%i.png" % page.number)
    
    if tkimg is not None:
     view_image.configure(image=tkimg,text=filename,compound=BOTTOM)
     view_image.image=tkimg
     view_image.text=filename
     view_image.compound = BOTTOM
     
    
     text = page.get_text('words')
     text_blocks = page.get_text('blocks')
     coutt = 1
     for i in text_blocks:
      x = i[0]
      y = i[1]
      w = i[2]
      h = i[3]
      
      
      if i[5]==1:
          retailer_info = i[4].split('\n')
          
          output['retailer_name'] = retailer_info[0]
          total_length = len(retailer_info)
          output['retailer_gstin'] = retailer_info[total_length-3].replace("GSTIN:","").strip()
          output['retailer_pan'] = retailer_info[total_length-2].replace("PAN:","").strip()
          output['retailer_address'] = "\n".join([retailer_info[m] for m in range(1,total_length-3)])
            
      if i[5]==2:
          id_info = i[4].split('\n')
          output['invoice_number']=id_info[0].replace("INVOICE NO:","")
          output['invoice_date']=id_info[1].replace("Dated :","")
          #print(output)
      if i[5]==5:
          ds_info = i[4].split('\n')
          output['description_of_services']=ds_info[1].strip()
          output['sac']=ds_info[2].strip()
          output['amount']=ds_info[3].strip()
          #print(output) 
      if i[5]==6:
          cgst = i[4].split('\n')
          output['cgst']=cgst[1].strip()
      
      if i[5]==7:
          sgst = i[4].split('\n')
          output['sgst']=sgst[1].strip()
      
      if i[5]==8:
          igst = i[4].split('\n')
          output['igst']=igst[1].strip()
      
      if i[5]==9:
          total = i[4].split('\n')
          output['total']=total[1].strip()
          
          #print(output)       
      
      if i[5]==14:
          otp = i[4].split('\n')
          output['otp']=otp[1].replace("OTP:","").strip()
          
          
          
         
              
      
     
      image = cv2.imread(r"page-%i.png" % page.number)
      
      start_point = (int(x),int( y))
      end_point = (int(w), int(h))
      color = (255, 0, 0)
      thickness = 2
      image = cv2.rectangle(image, start_point, end_point, color, thickness)
      image = cv2.putText(image, '{co}'.format(co=coutt), (int(x), int(y+20)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (36,255,12), 2)
      coutt = coutt+1
      cv2.imwrite(r"page-%i.png" % page.number, image)
     print(output)
     text = json.dumps(output, indent=2)
     view_text.configure(text=text)
     view_text.text=text
     
    cv2.imshow(r"page-%i.png" % page.number, image) 
    # view_image.configure(image=image,text=filename,compound=BOTTOM)
    # view_image.image=image
    # view_image.text=filename
    # view_image.compound = BOTTOM
    
     

        
        
    pass

upload_button.config(command=upload)


window.mainloop();