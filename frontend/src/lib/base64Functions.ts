export function base64Decoder(input: string): string {
    const decoded = atob(input);
    return decoded;
}

export function base64Encoder(input: string): string {
    const encoded = btoa(input);
    return encoded;
}