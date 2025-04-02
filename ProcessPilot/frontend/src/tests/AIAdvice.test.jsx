import { render, screen, fireEvent } from "@testing-library/react";
import AIAdvice from "../components/AIAdvice";

test("renders AIAdvice component", () => {
  render(<AIAdvice />);
  expect(
    screen.getByText(/Hi! How can I assist you today?/i)
  ).toBeInTheDocument();
});

test("sends a query to the backend", async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () =>
        Promise.resolve({ response: "<b>Current CPU usage is 15%.</b>" }),
    })
  );

  render(<AIAdvice />);
  const input = screen.getByPlaceholderText(/Type your message.../i);
  const button = screen.getByText(/Send/i);

  fireEvent.change(input, { target: { value: "What is my CPU usage?" } });
  fireEvent.click(button);

  expect(
    await screen.findByText(/Current CPU usage is 15%./i)
  ).toBeInTheDocument();
});
