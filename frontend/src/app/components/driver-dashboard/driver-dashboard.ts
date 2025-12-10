import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DriverService } from '../../services/driver.service';
import { AuthService } from '../../services/auth.service';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-driver-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './driver-dashboard.html',
  styleUrl: './driver-dashboard.css',
})
export class DriverDashboard implements OnInit {
  currentTrip: any = null;
  history: any[] = [];
  currentUser: any = null;
  loading = false;

  private driverService = inject(DriverService);
  private authService = inject(AuthService);
  private toastService = inject(ToastService);

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      if (user) {
        this.loadData();
      }
    });
  }

  loadData() {
    this.loading = true;
    this.driverService.getCurrentTrip(this.currentUser.idUsuario).subscribe({
      next: (data) => {
        this.currentTrip = data;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
      }
    });

    this.driverService.getTripHistory(this.currentUser.idUsuario).subscribe({
      next: (data) => this.history = data,
      error: (err) => console.error(err)
    });
  }

  startTrip() {
    if (!this.currentTrip) return;
    if (confirm('¿Iniciar el viaje ahora?')) {
      this.driverService.startTrip(this.currentTrip.idViaje, this.currentUser.idUsuario).subscribe({
        next: (res) => {
          this.toastService.show('¡Viaje iniciado!', 'success');
          this.loadData();
        },
        error: (err) => this.toastService.show('Error al iniciar viaje', 'error')
      });
    }
  }

  endTrip() {
    if (!this.currentTrip) return;
    if (confirm('¿Finalizar el viaje?')) {
      this.driverService.endTrip(this.currentTrip.idViaje, this.currentUser.idUsuario).subscribe({
        next: (res) => {
          this.toastService.show('Viaje finalizado correctamente', 'success');
          this.loadData();
        },
        error: (err) => this.toastService.show('Error al finalizar viaje', 'error')
      });
    }
  }
}
