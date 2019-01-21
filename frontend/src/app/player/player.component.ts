import { Component, Input } from '@angular/core';
import { AlertService, PlayerService } from '../_services';
import { User } from '../_models';
import { first } from "rxjs/operators";

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent {

  @Input() currentUser: User;
  isShuffle = false;
  isLoop = false;

  constructor(private player: PlayerService, private alertService: AlertService) {
    this.shuffled();
    this.looped();
    this.update();
    setInterval(() => {
      this.shuffled();
      this.looped();
      this.update();
    }, 10000);
  }

  previous(event) {
    this.player.prev(this.currentUser.username).subscribe(data => {
        console.log(data);
      },
      err => {
        this.alertService.error(err);
      });
  }

  next(event) {
    this.player.next(this.currentUser.username).subscribe(data => {
        console.log(data);
      },
      err => {
        this.alertService.error(err);
      });
  }

  playPause(event) {
    this.player.playPause(this.currentUser.username)
      .pipe(first())
      .subscribe(data => {
        },
        err => {
          console.error(err);
          this.alertService.error(err);
        });
  }

  shuffle(event) {
    this.player.shuffle(this.currentUser.username)
      .pipe(first())
      .subscribe(data => {
          this.isShuffle = !this.isShuffle;
        },
        err => {
          console.log(err);
          this.alertService.error(err);
        });
  }

  loop(event) {
    this.player.loop(this.currentUser.username)
      .pipe(first())
      .subscribe(data => {
          this.isLoop = !this.isLoop;
        },
        err => {
          console.log(err);
          this.alertService.error(err);
        });
  }

  shuffled() {
    this.player.isShuffle()
      .pipe(first())
      .subscribe(data => {
          this.isShuffle = data === 'true';
        },
        err => {
          console.log(err);
          this.alertService.error(err);
        });
  }

  looped() {
    this.player.isLoop()
      .pipe(first())
      .subscribe(data => {
          this.isLoop = data === 'true';
        },
        err => {
          console.log(err);
          this.alertService.error(err);
        });
  }

  update() {
    this.player.updatedb()
      .pipe(first())
      .subscribe(data => {
      }, err => {
        console.log(err);
        this.alertService.error(err);
      });
  }
}
