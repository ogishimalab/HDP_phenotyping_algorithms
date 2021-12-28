use strict;
use warnings;
use Text::ParseWords;
#HELLP症候群が含まれる場合をリストアップする
#全角の場合は？#
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
my $out = "HELLP症候群.csv";
open(OUT,">", $out) or die "$!";
my %dict;
my %dict2;
open(FH, $file) or die "$!";
while(<FH>){
	chomp;
	my @splited_line = &parse_line(",", undef, $_);		
	if(($splited_line[1] eq "XXXXX2") or ($splited_line[1] eq "XXXXX3") or ($splited_line[1] eq "XXXXX4")or ($splited_line[1] eq "XXXXX5") or ($splited_line[1] eq "XXXXX6")){
		my $sentence = $splited_line[6];
		my $jid = $splited_line[12];
		my @splited = split(/\s| |　|,|、|。|・|\//,$sentence);
		foreach my $each_item(@splited){	
			if((($each_item =~ /HELLP/) or ($each_item =~ /ＨＥＬＬＰ/)) and ($each_item !~ /考えにくい/) and ($each_item !~ /ではない/) and ($each_item !~ /なし/) and ($each_item !~ /否定的/)){
				if(defined $$id_dict{$jid}){
					print OUT $jid,",",$_,"\n";
				}
			}
		}
	}
}
