#coding:utf-8
#20170404:sort BP and PU data by weeks of pregnancy
import csv
import datetime
import sys
from heapq import merge
import numpy
import re

def checker_core(row, col_num, rep):
  flag = 0
  for num in col_num:
    data = row[num]
    if (data == "－"):
      data = "-"
    if ((data != "") and (int(data) != rep)):
      flag = 1	
      return flag    
  
def outelier_check(row, high_bp, row_bp):
  checker = 0
  for bp_row in high_bp:
    bp = row[bp_row]
    if ((bp != "") and ((int(bp) < 60) or (int(bp) > 200))):
      checker = 1
  for bp_row1 in row_bp:
    bp1 = row[bp_row1]
    if ((bp1 != "") and ((int(bp1) < 30) or (int(bp1) > 120))):
      checker = 1
  return checker
  

def conv_format(date_str):
  if date_str == "":
    a = ""
  else:
    date_splited = date_str.split("-")
    a = datetime.date(int(date_splited[0]), int(date_splited[1]), int(date_splited[2]))
  return a
def conv_format2(date_str):
  if date_str == "":
    a = ""
  else:
    date_splited = date_str.split("/")
    a = datetime.date(int(date_splited[0]), int(date_splited[1]), int(date_splited[2]))
  return a
def conv_format1(date_str):
  if date_str == "":
    a = ""
  else:
    date_splited = list(str(date_str))
    a = datetime.date(int("".join(date_splited[0:4])), int("".join(date_splited[4:6])), int("".join(date_splited[6:8])))
  return a  
 
def get_data_col(col_num_dict, label_names):
  d = []
  for l in label_names:
    if l in col_num_dict:
      l_list = col_num_dict[l]
      d = list(merge(d, l_list))
  return d
 
def get_conv_data(est_data, data_point):
  data_point = conv_format(data_point)
  diff = est_data - data_point
  diff_s = diff.days
  data_point_weeks = round(((280 - diff_s) / 7), 2)
  return data_point_weeks
 
def convert_date(file_name, outfile, col_num_dict):
  label_names = ["Measurement date(SBP)","Measurement date(DBP)","Measurement date(PU)"]
  data = get_data_col(col_num_dict, label_names)  
  o = open(outfile, 'w')
  count = 0
  est = get_colmn_nuns_core(col_num_dict, "Expected day")
  delv = get_colmn_nuns_core(col_num_dict, "Delivery day")
  f = csv.reader(open(file_name))
  for row in f:
    count+=1
    if count != 1:
      est_data = row[est[0]]
      del_date = row[delv[0]]
      if ((est_data != "") or (del_date != "")):
        if est_data == "":
          est_data = del_date
        if est_data != "" and len(est_data) == 8:
          est_data = conv_format1(est_data)
          #estimated date = 40 week * 7 day# 
          for each_data_point in data:
            data_point = row[each_data_point]
            if data_point != "" and str(data_point) != "0.0":
              data_point_weeks = get_conv_data(est_data, data_point)
              row[each_data_point] = data_point_weeks
          jid = row[0]	
          row = list(map(lambda x: str(x), row))
          joined = ','.join(row) 		
          o.write(joined)
          o.write("\n")
        else:
          print(row[0])
    else:
      row = list(map(lambda x: str(x), row))
      joined = ','.join(row) 
      o.write(joined)
      o.write("\n")
	  
	  
def get_first_PIH_bp(val_p, week_p, row, th):
  bps = []
  weeks = []
  for x in range(0, len(val_p)):
    each_val_p = val_p[x]
    each_week_p = week_p[x]
    each_data = row[each_val_p]
    each_week = row[each_week_p]
    if each_data != "" and each_week != "":
      bps.append(each_data)
      weeks.append(each_week)
  bps = list(map(lambda x: float(x), bps))
  weeks = list(map(lambda x: float(x), weeks))
  sorted_bps, sorted_weeks = week_sort(bps,weeks)	
  for x in range(0, len(sorted_bps)):
    each_data = sorted_bps[x]
    each_weeks = sorted_weeks[x]
    if each_data != "":
      if (int(each_data) >= th):
        first_week = int(float(each_weeks))
        return first_week
  first_week = 100		
  return first_week

def week_sort(datas, weeks):
  sort_index = numpy.argsort(weeks)
  datas = numpy.array(datas)
  sorted_data = datas[sort_index]
  sorted_weeks = sorted(weeks)
  sorted_data = list(sorted_data)
  return sorted_data, sorted_weeks
  
def get_first_PIH_pu(pu, pu_week, row):
  pus = []
  weeks = []
  for x in range(0, len(pu)):
    each_val_point = pu[x]
    each_week_point = pu_week[x]
    each_val = row[each_val_point]
    each_week = row[each_week_point]
    if each_val != "" and each_week != "":
      pus.append(each_val)	
      weeks.append(each_week)
  weeks = list(map(lambda x: float(x), weeks))
  sorted_pus, sorted_weeks = week_sort(pus,weeks)	
  for x in range(0, len(sorted_pus)):
    each_val = sorted_pus[x]
    each_week = sorted_weeks[x]
    if each_val != "":
      if ((each_val == "03") or (each_val == "04") or (each_val == "05")):
        first_week = int(float(each_week))
        if first_week >= 20:
          return first_week
  first_week = 100		  
  return first_week

def get_first_week(h_week, l_week):
  if h_week >= l_week:
    return l_week
  else:
    return h_week

def get_onset_week(hp_week, pu_week):
  if int(hp_week) >= int(float(pu_week)):
    return int(float(hp_week))
  else:
    return int(float(pu_week))

def hp_checker(row, high_bp, low_bp):
  check = 0
  for x in range(0, len(high_bp)):
    high_data_point = high_bp[x]
    if (row[high_data_point] != ""):
      if int(row[high_data_point]) >= 140:
        check = 1		
  for y in range(0, len(low_bp)):
    low_data_point = low_bp[y]
    if (row[low_data_point] != ""):
      if int(row[low_data_point]) >= 90:
        check = 1
  return check
  
def row_converter(row, data_point, week_point):
  for x in range(0, len(data_point)):
    each_data_point = data_point[x]
    each_week_point = week_point[x]
    if row[each_data_point] != "":
      if int(row[each_data_point]) == 0:
        row[each_data_point] = ""
        row[each_week_point] = ""
  return row		
	
def setting_checker(val_p, week_p):
  if (len(val_p) != len(week_p)):
    print("OMG1")
    sys.exit()


def get_colmn_nuns_core(col_num_dict, colname):
  if colname in col_num_dict:
    col = col_num_dict[colname]
    return col
  else:
    return []
  
def sorter(data, week):
  c = numpy.argsort(numpy.array(week))
  data = numpy.array(data)[c]
  data = list(data)
  week.sort()
  return data, week
  
def bp_null_check(high_bp, row_bp,  row, id):  
  check = 1
  for x in range(0, len(high_bp)):
    high_data_point = high_bp[x]
    if ((row[high_data_point] != "") and (row[high_data_point] != 0)):
      check = 0
      return check
  for x in range(0, len(row_bp)):
    row_data_point = row_bp[x]
    if ((row[row_data_point] != "") and (row[row_data_point] != 0)):
      check = 0
      return check	  
  return check

def get_bp_week(bp_week1, bp_week2):
  if bp_week1 == "100":
    return bp_week2
  elif bp_week2 == "100":
    return bp_week1
  else:
    if bp_week1 >= bp_week2:
      return bp_week2
    else:
      return bp_week1

  
def get_first_week_cond(wo_pu_cond_id_dict, id):
   dict = wo_pu_cond_id_dict[id]
   week_list = dict.keys()
   week_list = sorted(week_list)
   first_week = week_list[0]
   return (first_week)
   
def phenotyping(file, classed, col_num_dict,ht_dict, wo_pu_cond_id_dict):
  high_bp = get_colmn_nuns_core(col_num_dict, "SBP")
  high_bp_week = get_colmn_nuns_core(col_num_dict, "Measurement date(SBP)")
  row_bp = get_colmn_nuns_core(col_num_dict, "DBP")
  row_bp_week = get_colmn_nuns_core(col_num_dict, "Measurement date(DBP)")
  pu = get_colmn_nuns_core(col_num_dict, "PU")
  pu_week = get_colmn_nuns_core(col_num_dict, "Measurement date(PU)")
  f = csv.reader(open(file))
  o = open(classed, 'w')
  count = 0
  hp_counter = 0
  m1_normal_counter = 0
  healthy = []
  ga = {}
  na = []
  chronic = []
  lo_pih = []
  eo_pih = []
  gh = []
  super_imposed_eo = []
  super_imposed_lo = []
  eo_gestational_hypertension = []
  lo_gestational_hypertension = []
  eo_pe = []
  lo_pe = []
  week_dict = {}
  for row in f:
    pih_class = ""
    m1_missing = 0
    count += 1
    if count == 1:
      joined = ','.join(row)
      o.write(joined)
      o.write("\n")
    else:
      row = row_converter(row, high_bp, high_bp_week)
      row = row_converter(row, row_bp, row_bp_week)
      outel = outelier_check(row, high_bp, row_bp)
      id = row[0]
      bp_null_flag = bp_null_check(high_bp, row_bp, row, id)
      if bp_null_flag != 1:
        if id in ht_dict:
          pu_week_ret = get_first_PIH_pu(pu, pu_week, row)
          if pu_week_ret == 100:
            sysdis_flag = get_sys_dis(id, wo_pu_cond_id_dict, bp_week)
            if sysdis_flag == 1:		  
              week = wo_pu_cond_id_dict[id]
              ga[id] = week							  				
              if week < 34:
                super_imposed_eo.append(id)
                pih_class = "SP EO"
                row.append(pih_class)
              else:
                pih_class = "SP LO"
                row.append(pih_class)
                super_imposed_lo.append(id)
            else:	
              pih_class = "CH"
              chronic.append(id)		  
              row.append(pih_class)
          else:
            #Super imposed hypertension#
			#chronic hypertension before pregnancy + protein uria
            if pu_week_ret < 34:
              super_imposed_eo.append(id)
              pih_class = "SP EO"
              row.append(pih_class)
            else:
              pih_class = "SP LO"
              row.append(pih_class)
              super_imposed_lo.append(id)
        else:
          check = hp_checker(row, high_bp, row_bp)
          if check == 0:
            pih_class = "Normotensive"
            row.append(pih_class)
          else:
            hp_counter += 1	  
            high_bp_week_ret = get_first_PIH_bp(high_bp, high_bp_week, row, 140)
            low_bp_week_ret = get_first_PIH_bp(row_bp, row_bp_week, row, 90)
            pu_week_ret = get_first_PIH_pu(pu, pu_week, row)		
            bp_week = get_first_week(high_bp_week_ret, low_bp_week_ret)
            if (bp_week >= 20):
              if pu_week_ret == 100:
                sysdis_flag = get_sys_dis(id, wo_pu_cond_id_dict, bp_week)
                if sysdis_flag == 1:
                  week = wo_pu_cond_id_dict[id]				
                  ga[id] = week							  				
                  if week < 34:
                    super_imposed_eo.append(id)
                    pih_class = "PE EO"
                    row.append(pih_class)
                  else:
                    pih_class = "PE LO"
                    row.append(pih_class)
                    super_imposed_lo.append(id)
                else:
                  #Gestational hypertension#
                  if (bp_week < 34):
                    eo_gestational_hypertension.append(id)
                    pih_class = "GH EO"
                    row.append(pih_class)
                  else:
                    lo_gestational_hypertension.append(id)
                    pih_class = "GH LO"
                    row.append(pih_class)
              else:
                #Preeclampsia#
                onset_week = get_onset_week(bp_week, pu_week_ret)
                if onset_week < 34:
                  pih_class = "PE EO"
                  eo_pe.append(id)
                  row.append(pih_class)
                else:
                  pih_class = "PE LO"
                  lo_pe.append(id)
                  row.append(pih_class)		         
            else:
              #Chronic hypertension#
              if pu_week_ret == 100:
                sysdis_flag = get_sys_dis(id, wo_pu_cond_id_dict, bp_week)
                if sysdis_flag == 1:
                  week = wo_pu_cond_id_dict[id]
                  ga[id] = week							  
                  if week < 34:
                    super_imposed_eo.append(id)
                    pih_class = "SP EO"
                    row.append(pih_class)
                  else:
                    pih_class = "SP LO"
                    row.append(pih_class)
                    super_imposed_lo.append(id)			  
                else:
                  chronic.append(id)
                  pih_class = "CH"
                  row.append(pih_class)
              else:
              #Super imposed hypertension#			
                onset_week = get_onset_week(bp_week, pu_week_ret)
                if onset_week < 34:
                  super_imposed_eo.append(id)
                  pih_class = "SP EO"
                  row.append(pih_class)
                else:
                  pih_class = "SP LO"
                  row.append(pih_class)
                  super_imposed_lo.append(id)
        row.append(str(outel))
        joined = ','.join(row)
        o.write(joined)
        o.write("\n")

def get_colomn_num(file):
  def get_dict_core(a):
    count = 0
    dict = {}
    for d in a:
      if d in dict:
        label_list = dict[d]
        label_list.append(count)
        dict[d] = label_list
      else:
        label_list = [count]
        dict[d] = label_list
      count += 1
    return dict

  f = csv.reader(open(file))
  count = 0
  for row in f:
    count += 1
    if count == 1:
      col_num_dict = get_dict_core(row)
      return col_num_dict


def get_action_date(file):
  f = csv.reader(open(file))
  action_dict = {}
  for row in f:
    j_id = row[0]
    date = row[3]
    action_dict[j_id] = date
  return action_dict
	
def get_ht_ids(file):
  f = csv.reader(open(file))
  action_dict = {}
  for row in f:
    j_id = row[0]
    data = row[1]
    action_dict[j_id] = 1
  return action_dict

def get_ids(wopu_cond, exp_dict, dict):
  def calc_week(cls_date, exp_date):
    exp_date = conv_format1(exp_date)
    cls_date = conv_format(cls_date)
    diff = exp_date - cls_date
    diff_s = diff.days
    data_point_weeks = round(((280 - diff_s) / 7), 2)
    return data_point_weeks	
  def update_dict(dict, id, week):
    if not id in dict:
      week_dict = {}
      week_dict[week] = 1
      dict[id] = week_dict
    else:
      week_dict = dict[id]
      week_dict[week] = 1
      dict[id] = week_dict	  
    return (dict)	
  f = csv.reader(open(wopu_cond))
  for row in f:
    id = row[0]
    cls_date = row[12]
    exp_date = exp_dict[id]
    if cls_date != "":
      week = calc_week(cls_date, exp_date)
      dict = update_dict(dict, id, week)
  return (dict)
  
def get_wopu_cond_ids(wopu_cond1, wopu_cond2, wopu_cond3, wopu_cond4, wopu_cond5, wopu_cond6, exp_dict):
    dict = {}
    dict = get_ids(wopu_cond1, exp_dict, dict)
    dict = get_ids(wopu_cond2, exp_dict, dict)
    dict = get_ids(wopu_cond3, exp_dict, dict)
    dict = get_ids(wopu_cond4, exp_dict, dict)
    dict = get_ids(wopu_cond5, exp_dict, dict)
    dict = get_ids(wopu_cond6, exp_dict, dict)
    return (dict)
def get_exp_date(file):
  dict = {}
  count = 0
  est = get_colmn_nuns_core(col_num_dict, "予定日")
  delv = get_colmn_nuns_core(col_num_dict, "出産日")
  f = csv.reader(open(file))
  for row in f:
    count+=1
    if count != 1:
      id = row[0]
      est_data = row[est[0]]
      del_date = row[delv[0]]
      if ((est_data != "") or (del_date != "")):
        if est_data == "":
          est_data = del_date
        if est_data != "" and len(est_data) == 8:
          dict[id] = est_data
  return (dict)
		  
def get_sys_dis(id, bd_dict, bp_week):
  sys_dis_flag = 0
  if id in bd_dict:
    bd_point = bd_dict[id]
    bp_week = float(bp_week)
    bd_point = float(bd_point)
    if bp_week <= bd_point:
      sys_dis_flag = 1
  return sys_dis_flag

		  
def get_bd_dict(file):
  f = csv.reader(open(file))
  action_dict = {}
  for row in f:
    j_id = row[0]
    week = row[1]
    action_dict[j_id] = week
  return action_dict		  
		  
file = "input_file.csv"
col_num_dict = get_colomn_num(file)
out = "converdate_date.csv"
classed = "phenotyped.csv"
ht = "hts.csv"
bd = "body_dist.withGA.csv"


exp_dict = get_exp_date(file)
bd_dict = get_bd_dict(bd)
ht_dict = get_ht_ids(ht)
convert_date(file, out, col_num_dict)
phenotyping(out, classed, col_num_dict, ht_dict, bd_dict)