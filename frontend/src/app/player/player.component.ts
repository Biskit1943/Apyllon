import { Component, OnInit } from '@angular/core';
import {PlayerService, AlertService} from '../_services';
import {first, map} from 'rxjs/operators';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

  constructor(private player: PlayerService, private alertService: AlertService) {
  }

  previous(event) {
    this.player.getPrev().subscribe(data => {
      console.log(data);
    },
      err => {
      console.log(err);
      });
  }
  ngOnInit() {
  }

}
