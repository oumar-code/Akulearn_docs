import React from "react";

export default function ContactPage() {
  return (
    <main>
      <header>
        <h1>Contact Us</h1>
        <p>We'd love to hear from you! Fill out the form below or reach us at [email@akudemy.com].</p>
      </header>
      <section>
        <form>
          <label htmlFor="name">Name:</label>
          <input id="name" name="name" type="text" required />
          <label htmlFor="email">Email:</label>
          <input id="email" name="email" type="email" required />
          <label htmlFor="message">Message:</label>
          <textarea id="message" name="message" required />
          <button type="submit">Send</button>
        </form>
        <p>[Replace with real contact handling or integration.]</p>
      </section>
    </main>
  );
}
