use strict;
use warnings;
use Text::ParseWords;

sub zero_flag{
	my ($each_item) = @_;
	my $med_check = 1;
	if($each_item =~ /.*短期間.*/){
		$med_check = 0;
	}
	if($each_item =~ /.*服用していない.*/){
		$med_check = 0;
	}
	if($each_item =~ /.*していた.*/){	
		$med_check = 0;
	}	
	return ($med_check);
}

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


my $data_file = "input_file.csv"
my $id_dict = get_id_dict($data_file);
my $file = "ht_candidate.csv";
my $out = "hts.csv";
my %dict;
open(FH, $file) or die "$!";
while(<FH>){
	chomp;
	my $med_check = 0;
	my @splited = split(/\s|,|　|、|。|・/,$_);
	foreach my $each_item(@splited){
		if($each_item =~ /((.*)高血圧(.*))/){
			my $item = $1;
			if($2 !~ /産褥|妊娠|父親|母親|弟|姉|妹|兄|叔父|叔母|祖父|祖母|祖父母/){
				if(not defined $3){
					$dict{$_}++;
				}
				else{
					if($3 !~ /症候群/){
						$dict{$_}++;
					}
				}
			}
		}
		if($each_item =~ /腎高内/){
			if($each_item !~ /甲状腺/){
				$dict{$_}++;
			}		
		}
		if($each_item =~ /降圧剤|アダラート|アムロジン|オルメテック|アルドメット|トランデート|ナトリックス|コニール|ニフェジピン|アプレゾリン/){
			$med_check = 1;
			$med_check = zero_flag($each_item);	
		}	
		if($med_check == 1){
			$med_check = zero_flag($each_item);
		}
		if($med_check == 1){
			$dict{$_}++;
		}
	}	
}

my @items = keys(%dict);
open(OUT,">",$out) or die "$!";
foreach my $item(@items){
	my ($jid, $data) = split(",", $item);
	if(defined $$id_dict{$jid}){
		print OUT $item,"\n";
	}
}