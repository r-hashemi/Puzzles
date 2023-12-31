
from IPython.display import display, HTML
from copy import copy, deepcopy


class Attrib:
    def __init__(self, attr_name, values):
        self.name=attr_name
        self.values=values
        self.linked_dict_names=[]

    def get_dic_name(self, name):
        return 'dic_'+name
    
    def get_dic(self, name):
        dict_name = self.get_dic_name(name)
        return getattr(self, dict_name)

    def add_other_attrib(self, attr :"Attrib"):
        dic={}
        for val in self.values :
            dic[val]= attr.values[:]

        dict_name = self.get_dic_name(attr.name)
        setattr(self, dict_name , dic)
        self.linked_dict_names.append(attr.name)

    def add_link_other_attrib(self, attr_name, val_self, val_other):
        dic_self = self.get_dic(attr_name)
        lst_singled_values=[]
        if len( dic_self[val_self])==1 and  dic_self[val_self][0]!= val_other:
            raise ValueError('setting value conflicted')
        l_pre=set( dic_self[val_self])
        dic_self[val_self]= val_other  if isinstance(val_other, list) else [val_other]
        if (len( dic_self[val_self])==1) and (len( dic_self[val_self])!=len(l_pre) ):
            print( f'{val_self} {dic_self[val_self]} has len 1')
            lst_singled_values.append( (attr_name, val_self, *dic_self[val_self]) )        
       
        if len(dic_self[val_self])==1:
            for val in self.values:
                if val!=val_self:
                    l_pre = set(dic_self[val])
                    dic_self[val] = list( set(dic_self[val])-set(dic_self[val_self]) )
                    if len(dic_self[val])!=len(l_pre):
                        print( f'{val} in  {attr_name} is reduced {l_pre-set(dic_self[val])}')
                        if len(dic_self[val])==1: 
                            lst_singled_values.append( (attr_name, val, *dic_self[val]) )
                            print( f'{val} in  {attr_name} is single  {dic_self[val]}')
        return lst_singled_values

    def remove_possible_values(self, attr_name, val_self, val_other):
        dic_self = self.get_dic(attr_name)
        if not isinstance(val_other,list):
            val_other=[val_other]

        lst_singled_values=[]
        l_pre = set(dic_self[val_self])
        dic_self[val_self]=list(set(dic_self[val_self])-set(val_other) )
        if len( dic_self[val_self])==0:
            raise ValueError('dic value empty')
        if  (len(dic_self[val_self])!=len(l_pre)):
            print( f'{val_self} in {attr_name} is reduced {l_pre-set(dic_self[val_self])}' )
            if len(dic_self[val_self])==1:
                lst_singled_values.append( (attr_name, val_self, *dic_self[val_self]) )
                print( f'{val_self} in  {attr_name} is single  {dic_self[val_self]}')

        if len(dic_self[val_self])==1:
            for val in self.values:
                if val != val_self:
                    l_pre = set(dic_self[val])
                    dic_self[val] = list( set(dic_self[val])-set(dic_self[val_self]) )
                    if (len(dic_self[val])!=len(l_pre) ):
                        print( f'{val} in  {attr_name} is reduced {l_pre-set(dic_self[val])}')
                        if len(dic_self[val])==1:
                            lst_singled_values.append( (attr_name, val, *dic_self[val]) )
                            print( f'{val} in  {attr_name} is single  {dic_self[val]}')
        return lst_singled_values

    def get_all_single_valued(self):
        single_valued=[]
        for link_name in self.linked_dict_names:
            dic = self.get_dic(link_name)
            for val in self.values:
                if len(dic[val])==1:
                    single_valued.append( (link_name, *dic[val], val))
        return single_valued



    # def __str__(self) -> str:
        # return self.name+'\n'.join(self.get_dic(dic_name).__str__() for dic_name in self.linked_dict_names)
    
    def __repr__(self) -> str:
        return self.name+': ' +'\n'.join(dic_name+': '+self.get_dic(dic_name).__str__() for dic_name in self.linked_dict_names)

class Zebra_Puzzle:

    def __init__(self):
        self.attr_names=[]        


    def get_attr_name(self, name):
        return  'attr_'+name
    
    def get_Attr(self, name):
        attr_name = self.get_attr_name(name)
        return getattr(self, attr_name)
    
    def add_attribute(self, name, attr_values): 
        attr = Attrib(name, attr_values) 
        attr_name = self.get_attr_name(name)
        setattr(self, attr_name, attr)

        for namei in self.attr_names:
            attri = self.get_Attr(namei)
            attri.add_other_attrib(attr)
            attr.add_other_attrib(attri)

        self.attr_names.append(name)

    def add_link_info(self, attr1_name, attr1_val, attr2_name, attr2_val, attr_names_prcs ): 
        attr1:Attrib = self.get_Attr(attr1_name)
        attr2:Attrib = self.get_Attr(attr2_name)

        # link one-one
        single_valued_1 = attr1.add_link_other_attrib( attr2.name, attr1_val, attr2_val)
        single_valued_2 = attr2.add_link_other_attrib( attr1.name, attr2_val, attr1_val)

        for dic_name, val1, val2 in single_valued_1:
            self.add_link_info( attr1.name, val1, dic_name, val2, set() )

        for dic_name, val1, val2 in single_valued_2:
            self.add_link_info( attr2.name, val1, dic_name, val2, set() )


        attr_names_prcs.update(set([attr1_name,attr2_name]))
        for attr_name in self.attr_names:
            if attr_name in attr_names_prcs:
                continue
            for attri, attri_val in zip([attr1, attr2],[attr1_val, attr2_val]):
                attrj, attrj_val = ( set(zip([attr1, attr2],[attr1_val, attr2_val])) - set([(attri, attri_val)])  ).pop() 
                dici = attri.get_dic(attr_name)
                if len(dici[attri_val])==1:
                    #attrk = self.get_Attr(attr_name)
                    attr_names_prcs.add(attr_name)
                    self.add_link_info( attrj.name, attrj_val, attr_name, *dici[attri_val], attr_names_prcs  )

                for vali in attri.values:
                    if vali == attri_val:
                        continue
                    if len(dici[vali])==1:
                        attrk = self.get_Attr(attr_name)
                        # dick = attrk.get_dic(attri.name)
                        single_valued_j = attrk.remove_possible_values( attrj.name, *dici[vali], attrj_val)
                        single_valued_k = attrj.remove_possible_values( attrk.name, attrj_val,*dici[vali] )

                        for dic_name, val1, val2 in single_valued_j:
                            self.add_link_info( attrk.name, val1, dic_name, val2, set()  )

                        for dic_name, val1, val2 in single_valued_k:
                            self.add_link_info( attrj.name, val1, dic_name, val2, set() )
  
    def get_all_single_links(self):
        single_links=[]
        for i,attri_name in enumerate(self.attr_names):
            attri = self.get_Attr(attri_name)
            for attrj_name in self.attr_names:
                if attri_name==attrj_name:
                    continue
                dici = attri.get_dic(attrj_name)
                for vali in attri.values:
                    if len(dici[vali])==1:
                        single_links.append( (attri_name, vali , attrj_name, *dici[vali]) )
                        print( vali , *dici[vali])
        return single_links

    def remove_possible_values(self, attr1_name, attr1_val, attr2_name, attr2_val):
        
        attr1:Attrib = self.get_Attr(attr1_name)
        single_valued = attr1.remove_possible_values(attr2_name, attr1_val,attr2_val)        
        for dic_name2, val1, val2 in single_valued:
            self.add_link_info( attr1.name, val1, dic_name2, val2, set() )

        attr2:Attrib = self.get_Attr(attr2_name)
        if not isinstance(attr2_val,list):
            attr2_val=[attr2_val]
        for attr2_vali in attr2_val:
            single_valued_i = attr2.remove_possible_values(attr1_name, attr2_vali, attr1_val )
            for dic_name2, val1, val2 in single_valued_i:
                self.add_link_info( attr1.name, val1, dic_name2, val2, set() )

    def check_neighborhood_solvable(self, attr1_name, attr1_val, attr2_name, attr2_val):
        attr1 = self.get_Attr(attr1_name)
        attr2 = self.get_Attr(attr2_name)

        if len(attr1.dic_Number[attr1_val])>1 and len(attr2.dic_Number[attr2_val])>1:
            return False
        if len(attr2.dic_Number[attr2_val])==1:
            attr1,attr1_name,attr1_val,  attr2,attr2_name,attr2_val = attr2,attr2_name,attr2_val, attr1,attr1_name,attr1_val

        house_num1 = attr1.dic_Number[attr1_val][0] 
        house_num2=-1
        if house_num1 ==1:
            house_num2=2
        elif house_num1==len(self.attr_names)-1:
            house_num2=len(self.attr_names)-2
        else:
            dic2 = self.attr_Number.get_dic(attr2.name)
            if len(dic2[house_num1+1])==1 and dic2[house_num1+1][0]!=attr2_val:
                house_num2 = house_num1-1
            elif len(dic2[house_num1-1])==1 and dic2[house_num1-1][0]!=attr2_val:
                house_num2=house_num1+1
            else:
                other_nums = list(set(dic2.keys())-set([house_num1-1,house_num1+1]))
                self.remove_possible_values( attr2.name, attr2_val,'Number',other_nums )
        
        if house_num2>0:
            self.add_link_info(attr2.name, attr2_val, "Number", house_num2, set() )
            return True
        
        return False
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
    
    def get_assoc_values(self, attr1_name, attr1_val, attr2_name):
        attr_1=self.get_Attr(attr1_name)
        dic_2=attr_1.get_dic(attr2_name)

        val = dic_2[attr1_val]
        return val
    
    def get_percentage_solved(self):
        n_solved=0
        n_tot=0

        for ki in range(0, len(self.attr_names) - 1):
            # Print categories on left
            k = self.attr_names[ki]
            attr_i = self.get_Attr(k)
            for i, att_val_i in enumerate(attr_i.values):
                # Print attributes on left
                for kj in range(1, len(self.attr_names)):
                    if kj<=ki:
                        continue
                    n_tot+=len(self.attr_names)-1
                    attr_j = self.get_Attr(self.attr_names[kj])
                    vals_i_j = self.get_assoc_values( attr_i.name, att_val_i, attr_j.name )   
                    n_solved+= len(self.attr_names)-1 - len( vals_i_j ) if len( vals_i_j )>1 else len(self.attr_names)-1
                    # for j, att2 in enumerate(attr_j.values):
                    #     if len(vals_i_j)==1:                         
                    #         if att2 in vals_i_j:
                    #             n_solved+=1
        return round(100*n_solved/n_tot,1) if n_tot>0 else 0
    
    def generate_matrix_html(self) -> str:
        # from IPython.display import display, HTML
        # Some css to make the table look nice
        table = """
    <style type="text/css">
    table, th, td {
      border: 1px solid black;
      margin: 0px;
      padding: 0px;
    }
    th 
    {
      vertical-align: bottom;
      text-align: center;
    }
    
    th span 
    {
      -ms-writing-mode: tb-rl;
      -webkit-writing-mode: vertical-rl;
      writing-mode: vertical-rl;
      transform: rotate(180deg);
      white-space: nowrap;
      spacing: 2px;
    }
    </style>
    """
        # Now generate the required HTML
        table += '<table>'
        # Print categories
        table += '<tr><th></th><th></th>'
        for ki in range(0, len(self.attr_names)):
            k = self.attr_names[ki]
            table += f"<th colspan='{len(self.attr_names):d}' style='text-align:center;'>{k}</th><th></th>"
        table += "</tr><tr><th></th><th></th>"
        # Print attributes
        for ki in range(0, len(self.attr_names) ):
            k = self.attr_names[ki]
            attr_k = self.get_Attr(k)
            for att in attr_k.values:
                table += f"<th class='rotate'><span>{att}</span></th>"
            table += "<th></th>"
        table += "</tr><tr>"
        # Print main body
        for ki in range(0, len(self.attr_names) ):
            # Print categories on left
            k = self.attr_names[ki]
            table += f"<th rowspan='{len(self.attr_names):d}'><span>{k}</span></th>"
            attr_k = self.get_Attr(k)
            for i, att in enumerate(attr_k.values):
                # Print attributes on left
                # it = ki * len(self.attr_names) + i
                table += f"<th>{att}</th>"
                for kj in range(0, len(self.attr_names)):
                    attr_j = self.get_Attr(self.attr_names[kj])                    
                    for j, att2 in enumerate(attr_j.values):
                        # Print values
                        if kj == ki:
                            c = "-"
                        else:
                            # jt = kj * len(self.attr_names) + j  
                            vals_i_j = self.get_assoc_values( attr_k.name, att, attr_j.name )                             
                            if len(vals_i_j)==1 and att2 in vals_i_j:                         
                                    c = 'o'
                            elif att2 not in vals_i_j:
                                    c='x'
                            else: 
                                    c = '.'
                        table += f"<td>{c}</td>"
                    table += f"<td>|</td>"
                table += "</tr><tr>"
            table += "<td>-</td>" * (2 + (len(self.attr_names) - 1) * (len(self.attr_names) + 1))
            table += "</tr><tr>"
        table += '</tr></table>'
        per = self.get_percentage_solved()
        table += f"Filled about {int(round(per)):d}% of the puzzle."
        return table

    def display_matrix(self):
        # Display output
        html_table = HTML(self.generate_matrix_html())
        display(html_table)

    def generate_table_determined(self,attr_name): 
       
        def str_pad(s):
            return s#.center(15,'-')
        
        table =''
        # Now generate the required HTML
        table += '<table>'
        # Print categories
        table += '<tr>'
        table += f"<th >{str_pad(' ')}</th>"
        attr = self.get_Attr(attr_name)
        for ki in range(0, len(attr.values)):
            k = attr.values[ki]
            table += f'<th style="text-align:center;width: 90px;font-size:20px">{str_pad(str(k))}</th>'
        table += "</tr>"
        for ki in range(0, len(self.attr_names) ):
            k = self.attr_names[ki]
            if k==attr_name:
                continue
            table += "</tr>"
            table += f'<td style="text-align:center;width: 90px;font-size:20px">{str_pad(k)}</td>'
            for kj in  attr.values:
                val_ki = self.get_assoc_values(attr_name, kj, k)
                if isinstance(val_ki[0],int):
                    val_ki=[ str(val) for val in val_ki]
                if len(val_ki)==1:
                    val= val_ki[0]
                else:                    
                    val=''.join(f'({v[0].upper()})' for v in val_ki)
                table += f'<td style="text-align:center;width: 90px;font-size:14px">{str_pad(val)}</td>'
            table += "</tr>"
        table += '</table>'
        return table

    def dispaly_table_determined(self, attr_name):
        html_table = HTML(self.generate_table_determined(attr_name))
        display(html_table)

