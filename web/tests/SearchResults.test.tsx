// import SearchResults from "../src/js/components/SearchResults";
// import { render, screen, userEvent } from "../src/js/utils/test-utils";

// describe("Simple working test", () => {
//   it("the title is visible", () => {
//     render(<SearchResults />);
//     expect(screen.getByText(/Hello Vite \+ React!/i)).toBeInTheDocument();
//   });

//   it("should increment count on click", async () => {
//     render(<SearchResults />);
//     userEvent.click(screen.getByRole("button"));
//     expect(await screen.findByText(/count is: 1/i)).toBeInTheDocument();
//   });

//   it("uses flexbox in searchResults header", async () => {
//     render(<SearchResults />);
//     const element = screen.getByRole("banner");
//     expect(element.className).toEqual("SearchResults-header");
//     expect(getComputedStyle(element).display).toEqual("flex");
//   });
// });
