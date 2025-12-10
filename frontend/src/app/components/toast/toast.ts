import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="toastService.toast$ | async as toast" class="toast-container" [ngClass]="toast.type">
      <div class="toast-content">
        <i class="fas" [ngClass]="{
            'fa-check-circle': toast.type === 'success',
            'fa-exclamation-circle': toast.type === 'error',
            'fa-info-circle': toast.type === 'info'
        }"></i>
        <span>{{ toast.text }}</span>
      </div>
      <button class="close-btn" (click)="toastService.clear()">&times;</button>
    </div>
  `,
  styles: [`
    .toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 20px;
      border-radius: 8px;
      color: white;
      font-family: 'Segoe UI', sans-serif;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      display: flex;
      align-items: center;
      gap: 15px;
      z-index: 9999;
      animation: slideIn 0.3s ease-out;
      min-width: 300px;
    }
    .toast-container.success { background-color: #2ecc71; }
    .toast-container.error { background-color: #e74c3c; }
    .toast-container.info { background-color: #3498db; }

    .toast-content {
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
    }
    .toast-content i { font-size: 1.2rem; }
    .toast-content span { font-weight: 500; font-size: 1rem; }

    .close-btn {
      background: none;
      border: none;
      color: white;
      font-size: 1.5rem;
      cursor: pointer;
      opacity: 0.7;
    }
    .close-btn:hover { opacity: 1; }

    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `]
})
export class ToastComponent {
  toastService = inject(ToastService);
}
