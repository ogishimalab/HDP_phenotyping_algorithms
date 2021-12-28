use strict;
use warnings;
use Text::ParseWords;
#肝機能障害が含まれる場合をリストアップする
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
my $file = "clinical_notes.csv";
my $out = "EBウイルス肝機能障害.csv";
open(OUT,">", $out) or die "$!";
my %dict;
my %dict2;
open(FH, $file) or die "$!";
while(<FH>){
	chomp;
	my @splited_line = &parse_line(",", undef, $_);		
	if($splited_line[1] eq "XXXXX1"){
		my $sentence = $splited_line[6];	
		my $jid = $splited_line[12];
		my @splited = split(/\s| |　|,|、|。|・|\//,$sentence);
		foreach my $each_item(@splited){	
			if($each_item =~ /EBウイルス肝機能障害/){
				if(defined $$id_dict{$jid}){
					print OUT $jid,",",$_,"\n";
				}
			}
		}
	}
}
