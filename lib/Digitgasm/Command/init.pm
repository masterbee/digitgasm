package Digitgasm::Command::deploy;

use Mojo::Base 'Mojolicious::Command';


sub run {
  my ($self, @args) = @_;

  my $app = $self->app;

  my $public = $app->home->child('public');
  
  $app->sqlite->migrations->migrate(defined $version ? $version : ());
}


1;