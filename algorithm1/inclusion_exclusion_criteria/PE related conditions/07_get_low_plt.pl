use strict;
use warnings;
use Text::ParseWords;
sub get_id_dict{
	my ($data_file) = @_;
	my $count = 0;
	my %dict;
	open(FH, $data_file) or die "$!";
	while(<FH>){
		chomp;
		$count++;
		if($count > 1){
			my @splited_line = &parse_line(',', undef, $_);
			my $id = $splited_line[0];
			$dict{$id}++;
		}
	}
	return (\%dict);
}

my $data_file = "input_file.csv";
my $id_dict = get_id_dict($data_file);
my %dict;
my $file = "clinical_notes.csv";
my $out = "lowPLT.csv";

open(OUT,">", $out) or die "$!";
open(FH, $file) or die "$!";
while(<FH>){
	chomp;
	my @splited_line = &parse_line(',', undef, $_);
	my $itemcd = $splited_line[1];
	my $result = $splited_line[6];
	my $jid = $splited_line[12];
	#XXXXX9=value of PLT
	if($itemcd eq "XXXXX9"){
		if((defined $result) and ($result ne "") and ($result ne "KSN|") and ($result ne "0.0") and ($result < 10)){
			if(defined $$id_dict{$jid}){
				my $ret = $jid . "," . $result;
				print OUT $jid,",",$_,"\n";		
			}		
		}	
	}
}
