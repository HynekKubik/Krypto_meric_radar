import aes
import time

start_v = time.time()
a = aes.menu_aes_base_impl("/home/hynek/Obrázky/pokus/pokus/1.png")
#print(len(a))
end_v = time.time()
print(end_v - start_v)

