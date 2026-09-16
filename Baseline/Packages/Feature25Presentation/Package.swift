// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature25Presentation",
    products: [.library(name: "Feature25Presentation", targets: ["Feature25Presentation"])],
    dependencies: [.package(path: "../Feature25Domain"),
        .package(path: "../Feature25Data")],
    targets: [.target(name: "Feature25Presentation", dependencies: [.product(name: "Feature25Domain", package: "Feature25Domain"), .product(name: "Feature25Data", package: "Feature25Data")])]
)
