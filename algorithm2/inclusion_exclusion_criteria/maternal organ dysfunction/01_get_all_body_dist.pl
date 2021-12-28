use strict;
use warnings;
use Text::ParseWords;


sub get_basal_history_ids{
	my ($dir) = @_;
	chdir($dir) or die "$!";
	my %dict;
	my @files = glob("*");
	foreach my $each_file(@files){
		open(FH, $each_file) or die "$!";
		while(<FH>){
			chomp;
			my @splited_line = split(",",$_);
			my $jid = $splited_line[0];
			$dict{$jid}++;
		}
	}
	print "肝・腎の基礎疾患をもつ妊婦（母親）は、".scalar(keys(%dict))."名\n";
	return (\%dict);
}

sub get_small{
	my ($cls_date, $bef_cls) = @_;
	$cls_date =~ s/-//g;
	$cls_date =~ s/\///g;
	$bef_cls =~ s/\///g;
	$bef_cls =~ s/-//g;
	if($cls_date > $bef_cls){
		my $year = substr($bef_cls, 0, 4);
		my $month = substr($bef_cls, 4, 2);
		my $day = substr($bef_cls, 6, 2);
		$bef_cls = $year . "-" . $month ."-". $day;
		return ($bef_cls);
	}
	else{
		my $year = substr($cls_date, 0, 4);
		my $month = substr($cls_date, 4, 2);
		my $day = substr($cls_date, 6, 2);
		$cls_date = $year . "-" . $month ."-". $day;	
		return ($cls_date);
	}
}

sub get_ids{
	my ($dict, $file, $cls_dict) = @_;
	open(FH, $file) or die "$!";
	while(<FH>){
		chomp;
		my @splited_line = &parse_line(',', undef, $_);
		my $jid = pop @splited_line;
		my $cls_date = pop @splited_line;
		$$dict{$jid}++;
		if(defined $$cls_dict{$jid}){
			my $bef_cls = $$cls_dict{$jid};
			$cls_date = get_small($cls_date, $bef_cls);
			$$cls_dict{$jid} = $cls_date;
		}
		else{
			$$cls_dict{$jid} = $cls_date;
		}
	}
	return ($dict,$cls_dict);
}


sub get_target_jid2{
	my ($file, $dict, $cls_dict) = @_;
	my $count = 0;
	open(FH, $file) or die "$!";
	while(<FH>){
		chomp;
		$count++;
		if($count > 1){
			my @splited_line = &parse_line(',', undef, $_);
			my $jid = $splited_line[12];
			my $result = $splited_line[6];
			my $cls_date = $splited_line[11];
			my $itemcd = $splited_line[1];
			#XXXXX10=item about subjects having HELLP syndrome
			if($itemcd eq "XXXXX10"){
				#02 =YES
				if(($result ne "")and ($result eq "02")){
					$$dict{$jid}++;
					if(defined $$cls_dict{$jid}){
						my $bef_cls = $$cls_dict{$jid};
						$cls_date = get_small($cls_date, $bef_cls);
						$$cls_dict{$jid} = $cls_date;
					}
					else{
						$$cls_dict{$jid} = $cls_date;
					}
				}
			}
		}
	}
	return ($dict,$cls_dict);				
}



sub get_lkdis_preg{
	my ($fileset, $file) = @_;
	my (%dict,%cls_date);
	foreach my $each_file(@{$fileset}){
		my ($dict,$cls_date) = get_ids(\%dict, $each_file,\%cls_date);
		%dict = %{$dict};
		%cls_date = %{$cls_date};
	}
	#合併症の有無 HELLP症候群　の取得#
	my ($dict,$cls_date) = get_target_jid2($file, \%dict, \%cls_date);
	%dict = %{$dict};
	%cls_date = %{$cls_date};
	
	print "妊娠中の肝・腎機能障害をもつ妊婦（母親）は、".scalar(keys(%dict))."名\n";
	return (\%dict, \%cls_date);
}

sub get_consult{
	my ($consult) = @_;
	my (%dict, %cls_dict);
	open(FH, $consult) or die "$!";
	while(<FH>){
		chomp;
		my @splited_line = split(",", $_);
		my $rsv = $splited_line[0];
		my $joincohort = $splited_line[2];
		my $cls_date = $splited_line[1];
		$dict{$rsv} = $joincohort;
		$cls_dict{$rsv} = $cls_date;
	}
	return (\%dict, \%cls_dict);
}

sub get_nurdis_preg{
	my ($file_list) = @_;
	my (%dict, %cls_date);
	foreach my $each_file(@{$file_list}){
		my ($dict,$cls_date) = get_ids(\%dict, $each_file, \%cls_date);
		%dict = %{$dict};
		%cls_date = %{$cls_date};
	}
	print "妊娠中の神経学的障害をもつ妊婦（母親）は、".scalar(keys(%dict))."名\n";
	return (\%dict,\%cls_date);
}

sub get_target_jid1{
	my ($file,  $dict, $consult_dict, $cls_dict, $cls_date_dict) = @_;
	my $count = 0;
	my $ret_count = 0;
	open(FH, $file) or die "$!";
	while(<FH>){
		chomp;
		$count++;
		if($count > 1){
			my $row = $_;
			$row =~ s/"//g;
			my @splited_line = split(",", $row);
			my $rsv = $splited_line[0];
			my $result = $splited_line[6];
			if(($result ne "")and ($result < 10)){
				my $jid = $$consult_dict{$rsv};			
				my $cls_date = $$cls_dict{$rsv};
				$$dict{$jid}++;
				$$cls_date_dict{$jid} = $cls_date;
				$ret_count++;
			}
		}
	}
	print $ret_count,"\n";
	return ($dict, $cls_date_dict);
}


sub get_other_dict{
	my ($file_list) = @_;
	my (%dict, %cls_date);
	foreach my $each_file(@{$file_list}){
		my ($dict, $cls_date) = get_ids(\%dict, $each_file, \%cls_date);
		%dict = %{$dict};
		%cls_date = %{$cls_date};
	}
	print "妊娠中のその他障害をもつ妊婦（母親）は、".scalar(keys(%dict))."名\n";
	return (\%dict, \%cls_date);
}

sub get_wb_dist{
	my ($bh_dict, $preg_lk_dict, $preg_nurv_dict, $preg_other_dict) = @_;
	my %dict;
	my @preg_lk_ids = keys(%{$preg_lk_dict});
	foreach my $each_id(@preg_lk_ids){
		if(not defined $$bh_dict{$each_id}){
			$dict{$each_id}++;
		}
	}
	my @preg_nurv_ids = keys(%{$preg_nurv_dict});
	my @preg_other_ids = keys(%{$preg_other_dict});
	foreach my $each_id(@preg_nurv_ids){
		$dict{$each_id}++;
	}
	foreach my $each_id(@preg_other_ids){
		$dict{$each_id}++;
	}
	print "妊娠中の全身性の障害をもつ妊婦（母親）は、".scalar(keys(%dict))."名\n";
	return (\%dict);
}

sub get_cls_date{
	my ($cls_date1, $cls_date2, $cls_date3) = @_;
	my %cls_date_dict;
	while(my ($jid, $date) = each %{$cls_date1}){
		if(defined $cls_date_dict{$jid}){
			my $bef = $cls_date_dict{$jid};
			my $small = get_small($date, $bef);
			$cls_date_dict{$jid} = $small;
		}
		else{
			$cls_date_dict{$jid} = $date;
		}
	}
	while(my ($jid, $date) = each %{$cls_date2}){
		if(defined $cls_date_dict{$jid}){
			my $bef = $cls_date_dict{$jid};
			my $small = get_small($date, $bef);
			$cls_date_dict{$jid} = $small;
		}
		else{
			$cls_date_dict{$jid} = $date;
		}
	}
	while(my ($jid, $date) = each %{$cls_date3}){
		if(defined $cls_date_dict{$jid}){
			my $bef = $cls_date_dict{$jid};
			my $small = get_small($date, $bef);
			$cls_date_dict{$jid} = $small;
		}
		else{
			$cls_date_dict{$jid} = $date;
		}
	}
	return (\%cls_date_dict);
}

my $dir = "get_basal_diseases/out";
my $out = "body_dist.csv";
my $file1 = "肝機能障害.csv";
my $file2 = "肝機能上昇傾向.csv";
my $file3 = "腎機能障害.csv";
my $file4 = "紹介.csv";
my $file5 = "心窩部.csv";
my $file6 = "HELLP症候群.csv";
my $file7 = "ネフローゼ症候群.csv";
my $file8 = "liver_test.csv";


my $file9 = "けいれん.csv";
my $file10 = "眼華閃発.csv";
my $file11 = "子癇.csv";
my $file12 = "視野.csv";
my $file13 = "視野狭窄.csv";
my $file14 = "高血圧後の頭痛.csv";
my $file15 = "痙攣.csv";

my $file16 = "肺水腫.csv";
my $file17 = "lowPLT.csv";


my @fileset1 = ($file1, $file2, $file3, $file4, $file5, $file6, $file7, $file8);
my @fileset2 = ($file9, $file10, $file11, $file12, $file13, $file14, $file15);
my @fileset3 = ($file16, $file17);


my $file = "clinical_notes.csv";
my $bh_dict = get_basal_history_ids($dir);

my ($preg_lk_dict, $cls_date1) = get_lkdis_preg(\@fileset1, $file);
my ($preg_nurv_dict, $cls_date2) = get_nurdis_preg(\@fileset2);
my ($preg_other_dict, $cls_date3) = get_other_dict(\@fileset3);

my $wb_dict = get_wb_dist($bh_dict, $preg_lk_dict, $preg_nurv_dict, $preg_other_dict);
my $cls_date_dict = get_cls_date($cls_date1, $cls_date2, $cls_date3);
open(OUT,">", $out) or die "$!";
my @jids = keys(%{$wb_dict});
foreach my $each_jid(@jids){
	my $cls = $$cls_date_dict{$each_jid};
	print OUT $each_jid,",",$cls,"\n";
}