import Feature11Domain

public enum Feature11DataRepository {
    public static func load(_ id: Int) -> Feature11DomainModel {
        Feature11DomainModel(id: id, title: "Feature 11")
    }
}
