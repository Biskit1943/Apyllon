import { Component, OnInit } from '@angular/core';
import { PlayerService, AlertService} from '../_services';

@Component({
  selector: 'app-sidebar-content-folders',
  templateUrl: './sidebar-content-folders.component.html',
  styleUrls: ['./sidebar-content-folders.component.css']
})
export class SidebarContentFoldersComponent implements OnInit {

  songs = [];
  constructor(private player: PlayerService, private alertService: AlertService) {
  }

  ngOnInit() {
    this.player.listSongs().subscribe(songs => {
      console.log(songs);
    }, err => {
      this.alertService.error(err);
    });
  }
}
