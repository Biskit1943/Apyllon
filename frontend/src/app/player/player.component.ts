import { Component, Input } from '@angular/core';
import {PlayerService, AlertService} from '../_services';
import { User } from '../_models';
@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent {

  @Input() currentUser: User;
  constructor(private player: PlayerService, private alertService: AlertService) {
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
    this.player.play(this.currentUser.username, 'play').subscribe(data => {
        console.log(data);
      },
      err => {
        this.alertService.error(err);
      });
  }
}
