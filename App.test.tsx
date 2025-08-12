import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

describe('App component', () => {
  it('renders the application title', () => {
    render(<App />);
    const heading = screen.getByText(/AI Career Pathways Advisor/i);
    expect(heading).toBeInTheDocument();
  });
});