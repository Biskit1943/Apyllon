import { Component, OnInit } from '@angular/core';
import { PlayerService, AlertService} from '../_services';

@Component({
  selector: 'app-sidebar-content-folders',
  templateUrl: './sidebar-content-folders.component.html',
  styleUrls: ['./sidebar-content-folders.component.css']
})
export class SidebarContentFoldersComponent implements OnInit {

  songs: any = [];
  constructor(private player: PlayerService, private alertService: AlertService) {
  }

  async ngOnInit() {
     this.songs = await this.player.listSongs();
  }

  async playSong(song) {
    this.player.playSong(song.meta.title);
  }
}
