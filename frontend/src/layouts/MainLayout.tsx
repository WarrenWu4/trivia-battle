interface MainLayoutProps {
    children: React.ReactNode | React.ReactNode[] | string;
}

export default function MainLayout({ children }: MainLayoutProps) {
    return (
        <div className="w-full h-full bg-white dark:bg-neutral-800 font-pixeloid text-black dark:text-white">
            <div className="w-full max-w-md mx-auto py-6 px-4">
                {children}
            </div>
        </div>
    )
}