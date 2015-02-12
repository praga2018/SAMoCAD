# -*- coding: utf-8; -*-
from math import sqrt, copysign
import src.sectors_alg as sectors_alg
from os import path
import wx
import copy
import calc #import mirrorCalc, mirror_lines, mirror_points, calc_angle, offset_line
#from object_object import Root_object 
#from get_conf import get_line_conf
#ЛИНИЯ
list_prop = ('color', 'width', 'layer', 'stipple', 'factor_stipple')
#dp = {'fill':0, 'width', 'layer':0, 'stipple':0, 'factor_stipple':0}
### Действия создания линии ###
class Line:
    def __init__(self, par):
        self.par = par
        self.risLine()
        
    def risLine(self):
        self.par.kill()
        self.par.resFlag = True
        self.par.old_func = (self.par.action, Line)
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.line)

        self.par.info.SetValue('Line - point 1:')
        self.par.info2.SetValue('Enter - stop')

    def line(self, e):
        #self.par.ex, self.par.ey = self.par.get_world_coords(e)
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Unbind(wx.EVT_MOTION)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.line2)
        self.par.c.Bind(wx.EVT_MOTION, self.dynamic)
        #self.par.command.focus_set()
        #self.par.set_coord()
        self.par.ex = self.par.x_priv
        self.par.ey = self.par.y_priv
        #self.par.c.bind_class(self.par.c,"<1>", self.line2)
        #self.par.c.bind_class(self.par.c,"<Shift-1>", self.line2_shift)
        #self.par.dialog.config(text = u'Line - next point:')
        self.par.info.SetValue('Line - next point:')
        #self.par.line_clone = True

    def dynamic(self, e):
        if not self.par.motion_flag:
            self.par.dynamic_data = []
            self.par.dynamic_color = []
            self.line2()
        self.par.motion(e)
        e.Skip()

    def line2_shift(self, event):#Ести нажат Shift если не режим орто - чертится в режиме орто + ловит не точку привязки, а ее проекцию на ось, если режим орто - чертится как без орто
        #self.par.command.focus_set()
        #self.par.ex2 = self.par.priv_coord[0]
        #self.par.ey2 = self.par.priv_coord[1]
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        #self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        #if self.par.ortoFlag == False:
            #self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        c_line(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,fill='white',width=3)
        self.par.ex = self.par.ex2
        self.par.ey = self.par.ey2
        self.par.set_coord()
        self.par.changeFlag = True
        self.par.enumerator_p()
        self.par.com = None
        self.par.command.delete(0, 'end')

    def line2(self, event = None):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        #self.par.ex2 = self.par.priv_coord[0]
        #self.par.ey2 = self.par.priv_coord[1]
        #self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        #self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        #self.par.set_coord()
        
        if self.par.trace_flag or self.par.trace_obj_flag:
            if self.par.trace_flag:
                self.par.trace_on = True
            #if self.par.tracing_obj_Flag:
                #self.par.trace_obj_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex, self.par.ey
            self.par.trace_x2, self.par.trace_y2 = self.par.ex2, self.par.ey2
        
        #if self.par.ortoFlag == True and self.par.com == None:
            #if len(self.par.find_privs) == 1:
                #self.par.ex2,self.par.ey2=self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        if event:
            temp = False
            self.par.dynamic_data = []
            self.par.dynamic_color = []
            #self.par.command.focus_set()
            '''
            c_line(
                self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,
                width = self.par.width,
                layer = self.par.layer,
                fill = self.par.color,
                stipple = self.par.stipple,
                factor_stipe = self.par.factor_stipe,
                in_mass = False,
                temp = False,
                   )
            '''
            #self.par.history_undo.append(('c_', self.par.Nline))
            ex = self.par.ex2
            ey = self.par.ey2
            event.Skip()
            #self.par.set_coord()
            #self.par.changeFlag = True
            #self.par.enumerator_p()
            #self.par.com = None
            #self.par.command.delete(0, 'end')
        else:
            temp = True
            ex = self.par.ex
            ey = self.par.ey
        #print temp
        c_line(
            self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,
            width = self.par.width,
            layer = self.par.layer,
            color = self.par.color,
            stipple = self.par.stipple,
            factor_stipple = self.par.factor_stipple,
            in_mass = False,
            temp = temp,
               )
        self.par.ex = ex
        self.par.ey = ey

### Отрисовка линии ###
def c_line(
            par, x1, y1, x2, y2,
            width,
            layer,
            color,
            stipple,
            factor_stipple,
            in_mass,
            temp = False,
            ):
    #print x1, y1, x2, y2
    #if factor_stipple == None:
        #factor_stipple = par.factor_stipple

    if stipple:
        norm_stipple = False
        for i in par.stipples:
            if par.stipples[i] == tuple(stipple):
                norm_stipple = True
            if par.stipples[i] and len(par.stipples[i]) == len(stipple):
                if norm_stipple:
                    break
                else:
                    factor_stipple = par.stipples[i][0]*stipple[0]
                    #print factor_stip, stipple
                    stipple = [x/factor_stipple for x in stipple]
                    norm_stipple = True
        if not norm_stipple:
            stipple = None
        else:
            dash = [x*factor_stipple for x in stipple]
    if not temp:
        #width = int(width)
        par.total_N+=1
        #id_dict = {}
        #list_coords = []
        #list_colors = []
        #list_width = []
        
        #if tip == 'norm':
        if not stipple:
            
            lines = ((x1,y1,x2,y2),)
            par.pointdata.extend([x1,y1,x2,y2])
            par.colordata.extend(color * 2)
            par.IDs.append(par.total_N)
            #list_width.extend(width)
            
            #tags = ('obj', par.Nline, 'sel'))
            #id_dict[id] = ('line', 'priv', 'lin')
            
        else:
            lines, pointdata, colordata, IDs = stipple_line(par, x1,y1,x2,y2, dash = dash, color = color, width = width)
            if not lines:
                
            #id_dict.update(id)
            ##id = par.c.create_line(x1,y1,x2,y2, width=3, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', par.Nline, 'sel'))
            #id_dict[id] = ('line', 'priv', 'lin')
            #else:
                return
            else:
                par.pointdata.extend(pointdata)
                par.colordata.extend(colordata)
                par.IDs.extend(IDs)
        '''
        elif tip == 'temp':
            width = 1
            layer = 'temp'
            color = 'gray'
            id = par.c.create_line(x1,y1,x2,y2,fill=fill,width=width,tags = ('obj', par.Nline, 'sel'))
            id_dict = id_dict[id] = ('line', 'priv', 'temp')
        '''
        object_line = Object_line(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
        #dict_prop = {k:v for k,v in locals().iteritems() if k in list_prop}
        #points = #par.coordinator_to_global([x1, y1, x2, y2])
        
        par.ALLOBJECT[par.total_N] = {
                                    'object':'line',
                                    #'tags':id_dict,
                                    'class':object_line,
                                    'sectors':[],
                                    'coords': ([x1,y1,x2,y2],),
                                    'lines': lines,
                                    }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()              #Обновить картинку
            par.c.Update()
        
    else:
        if stipple == None:
            par.dynamic_data.extend([x1,y1,x2,y2])
            par.dynamic_color.extend(color * 2)
            
            #par.c.create_line(x1,y1,x2,y2, fill=fill,width=width,tags = ('obj', 'temp'))
            
        else:
            lines, pointdata, colordata, IDs = stipple_line(par, x1,y1,x2,y2, dash = dash, color = color, width = width)
            #d_line(par, x1,y1,x2,y2, dash = dash, fill=fill,width=width,tags = ('obj', 'temp'))
            
            ##par.c.create_line(x1,y1,x2,y2, width=3, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))

### Отрисовка линии сложного типа ###    
def stipple_line(par, x1,y1,x2,y2, dash, color, width):
    lines = []
    pointdata = []
    colordata = []
    IDs = []
    #dash = map(par.coordinator2, dash)
    xm = min(x1, x2)
    ym = min(y1, y2)
    xb = max(x1, x2)
    yb = max(y1, y2)
    dx = x1 - x2
    dy = y1 - y2
    d_dx = x1
    d_dy = y1
    pos = 0
    one = 0
    while 1:
        pos+=1
        if pos == len(dash)+1:
            pos = 1
        d = dash[pos-1]
        try:
            dx0 = sqrt((d*d * dx*dx)/(dy*dy + dx*dx))
        except ZeroDivisionError:
            return None
        if dy == 0:
            dy0 = 0
        elif dx == 0:
            dy0 = d * copysign(1, dy)
        else:
            dy0 = dx0 * dy / dx
        i = 1
        if x1 < x2:
            i =- 1
        xi1 = d_dx
        yi1 = d_dy
        xi2 = xi1 - i * dx0
        yi2 = yi1 - i * dy0
        d_dx = xi2
        d_dy = yi2
        ex = [xi1, xi2]
        ey = [yi1, yi2]
        cor = False
        for u in ex:
            if xm <= u <= xb:
                pass
            else:
                ind = ex.index(u)
                del ex[ind]
                if u < xm:
                    u = xm
                else:
                    u = xb
                ex.insert(ind, u)
                cor = True
        for u in ey:
            if ym <= u <= yb:
                pass
            else:
                ind = ey.index(u)
                del ey[ind]
                if u < ym:
                    u = ym
                else:
                    u = yb
                ey.insert(ind, u)
                cor = True

        if xm <= ex[1] <= xb and xm <= ex[0] <= xb and ym <= ey[1] <= yb and ym <= ey[0] <= yb:
            if pos % 2 != 0:
                lines.append([ex[0],ey[0],ex[1],ey[1]])
                pointdata.extend([ex[0],ey[0],ex[1],ey[1]])
                colordata.extend(color * 2)
                if one:
                    IDs.append(0)
                else:
                    IDs.append(par.total_N)
                    one = 1
                #id = par.c.create_line(ex[0],ey[0],ex[1],ey[1], fill=fill,width=width,tags=tags)
                #id_dict[id] = ('line',)
            if cor:
                return lines, pointdata, colordata, IDs
                
        else:
            return lines, pointdata, colordata, IDs
            

class Object_line:
    def __init__(self, par, obj):
        self.par = par
        self.obj = obj

    def create_object(self, cd):
        c_line(self.par, cd['coord'][0], cd['coord'][1], cd['coord'][2], cd['coord'][3],
               cd['width'],
               cd['layer'],
               cd['color'],
               cd['stipple'],
               cd['factor_stipple'],
               temp = cd['temp'],
                   )
        
    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        cd['coord'][0], cd['coord'][1] = self.par.coordinator(cd['coord'][0], cd['coord'][1], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['coord'][2], cd['coord'][3] = self.par.coordinator(cd['coord'][2], cd['coord'][3], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['temp'] = False
        self.create_object(cd)
        
    ### Edit_prop method ###
    def save(self, dxf):
        cd = self.get_conf()
        cd['x1'] = cd['coord'][0]
        cd['y1'] = cd['coord'][1]
        cd['x2'] = cd['coord'][2]
        cd['y2'] = cd['coord'][3]
        e = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(stipple)s, color = '%(color)s', layer = %(layer)s)"
        e = (e % cd)
        if dxf:
            cd['color'] = dxf_colorer(cd['color'])
        return e, cd
            
    ### Edit_prop method ###
    def edit_prop(self, params):
        param_changed = False
        r_list = None
        cd = self.get_conf()
        for param in params:
            if param in cd:
                param_changed = True
                cd[param] = params[param]
        if param_changed == True:
            cd['temp'] = False
            self.create_object(cd)
            r_list = (self.obj, self.par.Nline)
        return r_list
                   
    ### Trim method ###
    def trim_extend(self, x, y, trim_extend):
        cd = self.get_conf()
        if trim_extend == 'Trim':
            self.par.c.delete('C'+self.obj)
            cNew = calc.trim_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x, y, cd['coord'])
        else:
            cNew = calc.extend_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, cd['coord'])
            
        if cNew:
            self.par.delete(elements = (self.obj,))
            cd['temp'] = False
            self.create_object(cd)
            
        return cNew
    
    ### Edit method ###
    def edit(self, event):
        cd = self.get_conf()
        xn, yn, xf, yf = calc.near_far_point(cd['coord'], self.par.ex, self.par.ey)
        cd['coord'][0] = xn
        cd['coord'][1] = yn
        cd['coord'][2] = xf
        cd['coord'][3] = yf
        cd['coord'][0] = self.par.ex2
        cd['coord'][1] = self.par.ey2
        self.par.ex3 = xf
        self.par.ey3 = yf
        if event:
            cd['temp'] = False
        else:
            cd['temp'] = True
        self.create_object(cd)
    
    ### Rotate methods ###    
    def rotateN(self, x0, y0, msin, mcos, angle):
        cd = self.get_conf()
        cd['coord'] = calc.rotate_lines(x0, y0, [cd['coord'],], msin = msin, mcos = mcos)[0]
        cd['temp'] = True
        self.create_object(cd)
       

    #def rotateY(self, x0, y0, msin, mcos, angle):
        #find = self.par.ALLOBJECT[self.obj]['id']
        #for i in find:
            #coord = self.par.c.coords(i)
            #coord = tuple(calc.rotate_lines(x0,y0, [coord,], msin = msin, mcos = mcos)[0])
            #self.par.c.coords(i, coord)

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        coord = self.get_coord()
        coord = calc.rotate_lines(x0,y0, [coord,], msin = msin, mcos = mcos)[0]
        c_line(self.par, coord[0], coord[1], coord[2], coord[3],
               width = 1,
               layer = 't',
               color = 'yellow',
               stipple = None,
               factor_stipple = None,
               temp = True,
               )
    
    ### Offset method ###
    def offset(self, pd, x3, y3):
        c = self.get_coord()
        x1i, y1i, x2i, y2i = calc.offset_line(c[0],c[1],c[2],c[3],pd, x3, y3)
        c_line(self.par, x1i, y1i, x2i, y2i)
        
    ### Mirror methods ###   
    def mirrorN(self, px1, py1, sin, cos):
        cd = self.get_conf()
        cd['coord'] = calc.mirror_lines(px1,py1, [cd['coord'],], sin, cos)[0]
        c_line(self.par, cd['coord'][0], cd['coord'][1], cd['coord'][2], cd['coord'][3],
               cd['width'],
               cd['layer'],
               cd['color'],
               cd['stipple'],
               cd['factor_stipple'],
               )

    def mirrorY(self, px1, py1, sin, cos):
        find = self.par.ALLOBJECT[self.obj]['id']
        for i in find:
            coord = self.par.c.coords(i)
            coord = tuple(calc.mirror_lines(px1,py1, [coord,], sin, cos)[0])
            self.par.c.coords(i, coord)

    def mirror_temp(self, px1, py1, sin, cos):
        coord = self.get_coord()
        coord = calc.mirror_lines(px1,py1, [coord,], sin, cos)[0]
        c_line(self.par, coord[0], coord[1], coord[2], coord[3],
               width = 1,
               layer = 't',
               color = 'yellow',
               stipple = None,
               factor_stipple = None,
               temp = True,
               )
        
    ### Copy method ###    
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj]#self.get_conf()
        x1 = cd['coords'][0][0] + d[0]
        y1 = cd['coords'][0][1] + d[1]
        x2 = cd['coords'][0][2] + d[0]
        y2 = cd['coords'][0][3] + d[1]
        #cd['coord'] = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(cd['coord'])]
        c_line(self.par, x1, y1, x2, y2,
               width = cd['width'],
               layer = cd['layer'],
               color = cd['color'],
               stipple = cd['stipple'],
               factor_stipple = cd['factor_stipple'],
               in_mass = True,
               temp = False,
               )
        
        
    def copy_temp(self, d):
        coord = list(self.par.ALLOBJECT[self.obj]['coords'][0])#self.get_coord()
        x1 = coord[0] + d[0]
        y1 = coord[1] + d[1]
        x2 = coord[2] + d[0]
        y2 = coord[3] + d[1]
        #cd['coord'] = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(cd['coord'])]
        c_line(self.par, x1, y1, x2, y2,
               width = 1,
               layer = 't',
               color = [255, 255, 0],
               stipple = None,
               factor_stipple = None,
               in_mass = True,
               temp = True,
               )
    ### Get configure ###
    #Принимает объект - линию, возвращает все его свойства
    def get_conf(self):
        cd = {}
        for i in self.par.ALLOBJECT[self.obj]:
            if i in list_prop:
                cd[i] = self.par.ALLOBJECT[self.obj][i]
        cd['class'] = self.par.ALLOBJECT[self.obj]['class']
        cd['object'] = self.par.ALLOBJECT[self.obj]['object'] #Потом нужно будет удалить!!!
        #for i in self.par.ALLOBJECT[self.obj]['id']:
            #if 'line' in self.par.ALLOBJECT[self.obj]['id'][i] and 'priv' in self.par.ALLOBJECT[self.obj]['id'][i]:
                #cd['coord'] = self.par.c.coords(i)
        #points = list(self.par.ALLOBJECT[self.obj]['points'])
        cd['coords'] = self.par.ALLOBJECT[self.obj]['coords']#self.par.coordinator_to_local(points)
        #cd['coord'] = [cd['coord'][0][0], cd['coord'][0][1], cd['coord'][1][0], cd['coord'][1][1]]
        return cd

    #Принимает объект - линия, возвращает координаты
    def get_coord(self):
        points = list(self.par.ALLOBJECT[self.obj]['points'])
        coord = self.par.coordinator_to_local(points)
        #for i in self.par.ALLOBJECT[self.obj]['id']:
            #if 'line' in self.par.ALLOBJECT[self.obj]['id'][i] and 'priv' in self.par.ALLOBJECT[self.obj]['id'][i]:
                #coord = self.par.c.coords(i)
        return coord
