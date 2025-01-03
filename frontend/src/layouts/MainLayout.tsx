interface MainLayoutProps {
    children: React.ReactNode | React.ReactNode[] | string;
}

export default function MainLayout({ children }: MainLayoutProps) {
    return (
        <div className="font-pixeloid w-full max-w-md mx-auto py-6 px-4">
            {children}
        </div>
    )
}