use strict;
use warnings;
use Text::ParseWords;

sub get_sd_dict{
	my ($file) = @_;
	my %dict;
	open(FH, $file) or die "$!";
	while(<FH>){
		chomp;
		my @splited_line = split(",", $_);
		my $id = $splited_line[1];
		my $sd = $splited_line[16];
		if((defined $sd) and ($sd ne "") and ($sd ne "#REF!") and ($sd ne "#VALUE!") and ($sd ne "*")){
			my $fgr;
			if($sd < -1.5){
				$fgr = 1;
			}
			else{
				$fgr = 0;
			}
			$dict{$id} = $fgr;
		}
	}
	return (\%dict);
}

sub get_ga{
	my ($file) = @_;
	my %dict;
	open(FH, $file) or die "$!";
	while(<FH>){
		chomp;
		my @splited_line = split(",", $_);
		my $cid = $splited_line[1];
		if($splited_line[5] ne ""){
			my $ga_week = $splited_line[5];
			my $ga_day = $splited_line[6];
			if($ga_day eq ""){
				$ga_day = 0;
			}
			my $ga = ($ga_week * 7 + $ga_day)/7;
			$dict{$cid} = $ga;
		}
	}
	return (\%dict);
}

my $sd_file = "taikakubirthlongcross_v1.1.nocr.csv";
my $out_fgr = "fgr_list.csv";
my $ga_dict = get_ga($sd_file);
my $sd_dict = get_sd_dict($sd_file);
my $data_file = "mother_dataset_duo2.csv";
open(OUT, ">", $out_fgr) or die "$!";
my @ids = keys(%{$sd_dict});
my %target_mam_ids;
foreach my $each_id(@ids){
	my $fgr_flag = $$each_id{$each_cid};
	my $ga = "";
	if(defined $$ga_dict{$each_cid}){
		$ga = $$ga_dict{$each_cid};
	}
	print OUT $each_id,",",$fgr_flag,",",$ga,"\n";
}
