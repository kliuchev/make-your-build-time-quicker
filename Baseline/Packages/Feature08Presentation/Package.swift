// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature08Presentation",
    products: [.library(name: "Feature08Presentation", targets: ["Feature08Presentation"])],
    dependencies: [.package(path: "../Feature08Domain"),
        .package(path: "../Feature08Data")],
    targets: [.target(name: "Feature08Presentation", dependencies: [.product(name: "Feature08Domain", package: "Feature08Domain"), .product(name: "Feature08Data", package: "Feature08Data")])]
)
