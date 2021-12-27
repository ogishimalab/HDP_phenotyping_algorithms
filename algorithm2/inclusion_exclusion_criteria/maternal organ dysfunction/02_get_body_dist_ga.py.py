#coding:utf-8
#20170404:sort BP and PU data by weeks of pregnancy
import csv
import datetime
import sys
from heapq import merge
import numpy

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
	 
def convert_date(file, col_num_dict, body_dist):
  f1 = csv.reader(open(body_dist))
  bodt_dist_dict = {}
  for row1 in f1:
    jid = row1[0]
    cls_date = row1[1]
    bodt_dist_dict[jid] = cls_date

  body_dist_week_dict = {}
  count = 0
  est = get_colmn_nuns_core(col_num_dict, "Expected day")
  delv = get_colmn_nuns_core(col_num_dict, "Delivery day")
  f = csv.reader(open(file))
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
          jid = row[0]
          if jid in bodt_dist_dict:
            cls_date = bodt_dist_dict[jid]
            #estimated date = 40 week * 7 day#
            data_point_weeks = get_conv_data(est_data, cls_date)
            if 0 <= data_point_weeks and data_point_weeks < 42:
              body_dist_week_dict[jid] = data_point_weeks
  return body_dist_week_dict
	 
def get_first_PIH_bp(val_p, week_p, row, th):
  first_week = 100
  bps = []
  weeks = []
  for x in range(0, len(val_p)):
    each_val_p = val_p[x]
    each_week = week_p[x]
    each_data = row[each_val_p]
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
  return first_week

def week_sort(datas, weeks):
  sort_index = numpy.argsort(weeks)
  datas = numpy.array(datas)
  sorted_data = datas[sort_index]
  sorted_weeks = sorted(weeks)
  sorted_data = list(sorted_data)
  return sorted_data, sorted_weeks

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

def get_colmn_nuns_core(col_num_dict, colname):
  if colname in col_num_dict:
    col = col_num_dict[colname]
    return col
  else:
    return []
  
def get_ht_ids(file):
  f = csv.reader(open(file))
  action_dict = {}
  for row in f:
    j_id = row[0]
    data = row[1]
    action_dict[j_id] = 1
  return action_dict
  
def get_bp_week(est_data, row, bp_date):
  bp_weeks = []
  for date_row in bp_date:
    date = row[date_row]
    if date == "":
      bp_weeks.append("")
    else:
      w = get_conv_data(est_data, date)
      bp_weeks.append(w)
  return (bp_weeks)
  
def get_headache_after_bp(file, col_num_dict, headache_dict, ht_dict):
  headache_dict_after_bp = {}
  est = get_colmn_nuns_core(col_num_dict, "Expected day")
  delv = get_colmn_nuns_core(col_num_dict, "Delivery day")  
  high_bp = get_colmn_nuns_core(col_num_dict, "SBP")
  high_bp_date = get_colmn_nuns_core(col_num_dict, "Measurement date(SBP)")
  row_bp = get_colmn_nuns_core(col_num_dict, "DBP")
  row_bp_date = get_colmn_nuns_core(col_num_dict, "Measurement date(DBP)")
  f = csv.reader(open(file))
  count = 0
  for row in f:
    count+=1
    if count != 1:
      est_data = row[est[0]]
      del_date = row[delv[0]]
      if ((est_data != "") or (del_date != "")):
        if est_data == "":
          est_data = del_date
        est_data = conv_format1(est_data)
        high_bp_week = get_bp_week(est_data, row, high_bp_date)	
        row_bp_week = get_bp_week(est_data, row, row_bp_date)
        check = hp_checker(row, high_bp, row_bp)
        if check == 1:
          row = row_converter(row, high_bp, high_bp_week)
          row = row_converter(row, row_bp, row_bp_week)
          jid = row[0]
          high_bp_week_ret = get_first_PIH_bp(high_bp, high_bp_week, row, 140)
          low_bp_week_ret = get_first_PIH_bp(row_bp, row_bp_week, row, 90)
          bp_week = get_first_week(high_bp_week_ret, low_bp_week_ret)
          if jid in headache_dict:
            rsv_dict = headache_dict[jid]
            for rsv in rsv_dict:
              if jid in ht_dict:
                headache_dict_after_bp[rsv] = 1
              else:
                headache_week = rsv_dict[rsv]
                if bp_week < headache_week:
                  headache_dict_after_bp[rsv] = 1
  print (len(headache_dict_after_bp.keys()))
  return headache_dict_after_bp
        
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
	
def make_output(file_in, file_out, body_dict_dict):
  o = open(file_out, 'w')
  f = csv.reader(open(file_in))
  for row in f:	
    jid = row[0]
    if jid in body_dict_dict:
        ga = body_dict_dict[jid]
        col = [jid, ga]
        col = list(map(lambda x: str(x), col))	
        joined = ",".join(col)
        o.write(joined)
        o.write("\n")

file = "input_file.csv"
body_dist = "body_dist.csv";
body_dist_ga = "body_dist.withGA.csv";

col_num_dict = get_colomn_num(file)
body_dict_dict = convert_date(file, col_num_dict, body_dist)
make_output(body_dist, body_dist_ga, body_dict_dict)