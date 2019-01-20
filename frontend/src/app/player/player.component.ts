import { Component, Input } from '@angular/core';
import {PlayerService, AlertService} from '../_services';
import { User } from '../_models';
import { first } from "rxjs/operators";
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
    this.player.playPause(this.currentUser.username)
      .pipe(first())
      .subscribe(data => {
        console.log(data);
      },
      err => {
      console.error(err);
        this.alertService.error(err);
      });
  }
}
