// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature02Presentation",
    products: [.library(name: "Feature02Presentation", targets: ["Feature02Presentation"])],
    dependencies: [.package(path: "../Feature02Domain"),
        .package(path: "../Feature02Data")],
    targets: [.target(name: "Feature02Presentation", dependencies: [.product(name: "Feature02Domain", package: "Feature02Domain"), .product(name: "Feature02Data", package: "Feature02Data")])]
)
