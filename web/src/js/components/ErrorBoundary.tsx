import React from "react";
import ErrorView from "../pages/ErrorView";

class ErrorBoundary extends React.Component {
    constructor(props: any) {
        super(props);

        this.state = {
            hasError: false
        };
    }

    static getDerivedStateFromError(error: any) {
        // Update state so the next render will show the fallback UI.
        return {
            hasError: true
        };
    }

    render() {
        // @ts-ignore
        return this.state.hasError ? <ErrorView /> : this.props.children;
    }
}

export default ErrorBoundary;
