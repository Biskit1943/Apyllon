import { Component, Input } from '@angular/core';
import { AlertService, PlayerService } from '../_services';
import { User } from '../_models';

@Component({
    selector: 'app-player',
    templateUrl: './player.component.html',
    styleUrls: ['./player.component.css']
})
export class PlayerComponent {

    @Input() currentUser: User;
    private isShuffle = false;
    private isLoop = false;
    private currentSong = '';
    private currentArtist = '';
    private nextSong = '';
    private previousSong = '';
    private playing = false;

    constructor(private player: PlayerService, private alertService: AlertService) {
        this.player.getState().then((res) => {
            if (res && res.hasOwnProperty('state')) {
                this.update(res);
            }
            setInterval(async () => {
                this.update(await this.player.getState());
            }, 2000);
        }).catch(err => {
            this.alertService.error(err);
            console.log(err);
        });
    }

    async previous(event) {
        const state = this.update(await this.player.prev());
    }

    async next(event) {
        const state = this.update(await this.player.next());
    }

    async playPause(event) {
        try {
            let state;
            if (this.playing) {
                state = await this.player.stop();
            } else {
                state = await this.player.play();
            }
            this.update(state);
        } catch (err) {
            this.alertService.error(err);
            console.log(err);
        }
    }

    async shuffle(event) {
        try {
            this.update(await this.player.shuffle());
        } catch (err) {
            this.alertService.error(err);
            console.log(err);
        }
    }

    async loop(event) {
        try {
            this.update(await this.player.loop());
        } catch (err) {
            this.alertService.error(err);
            console.log(err);
        }
    }

    async shuffled() {
        try {
            this.isShuffle = await this.player.isShuffle();
        } catch (err) {
            console.log(err);
        }
    }

    async looped() {
        try {
            this.isLoop = await this.player.isLoop();
        } catch (err) {
            console.log(err);
        }
    }

    async update(state) {
        try {
            if (state && state.hasOwnProperty('shuffle') && state.hasOwnProperty('loop')) {
                this.playing = state['state'] === 'play';
                this.isLoop = state['loop'] === 'true';
                this.isShuffle = state['shuffle'] === 'true';
                this.currentSong = state['current'] ? state['current'].meta.title : null;
                this.nextSong = state['next'] ? state['next'].meta.title : null;
                this.previousSong = state['previous'] ? state['previous'].meta.title : null;
            }
        } catch (err) {
            console.log(err);
        }
    }
}
