from django.core.paginator import Paginator

objects = ['sdsd','sfsdf','dfedfdf','dfsfds','fdasfsa','aSDFaf']

p = Paginator(objects,2)

print(p.count)

p.get_page(1)