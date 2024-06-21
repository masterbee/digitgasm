package Digitgasm::Command::init;

use Mojo::Base 'Mojolicious::Command';
use Mojo::JSON qw(decode_json);
use Math::Combinatorics;
use Mojo::CSV;

use List::Util qw(sum);
use List::MoreUtils ':all';

sub run {
  my ($self, @args) = @_;

  my $app = $self->app;

  my $public = $app->home->child('public');

  foreach my $draw ($public->child('draws')->list({dir => 1})->each) {
      # lets establish some scoped variables
      my $config = decode_json $draw->child('index.json')->slurp;
      my $csv = Mojo::CSV->new( out => $draw->child('all.csv')->to_string );
      my @headers = ();

      # establish base headers
      push( @headers, 'slot-'.$_) for (1 .. $config->{combinations}->{draw});

      # add additional headers (augemented)
      push( @headers, $_) for ('sum','even-odd','low-high');

      $csv->trickle([ @headers ]);

      # set up combinations generator
      my $mixer = Math::Combinatorics->new(count => $config->{combinations}->{draw},
                                           data => [ $config->{combinations}->{to} .. $config->{combinations}->{from} ]
                                          );

      while(my @combo = $mixer->next_combination){
        my $sum = sum(@combo);
        my ($even, $odd) = (
            scalar(indexes { $_ % 2 == 0 } @combo) // 0,
            scalar(indexes { $_ % 2 != 0 } @combo) // 0,
          );

        push(@combo, $sum);
      }

  }
 
}


1;